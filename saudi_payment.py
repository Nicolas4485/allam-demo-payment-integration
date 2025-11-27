// ملف: saudiPayment.js
// المتطلبات: npm i axios luxon

import axios from 'axios';
import { DateTime } from 'luxon';

// ثابت: نسبة ضريبة القيمة المضافة في السعودية 15%
const SAUDI_VAT_RATE = 0.15;
// ثابت: المنطقة الزمنية للرياض
const RIYADH_TZ = 'Asia/Riyadh';

// دالة مساعدة: تحويل مبلغ بالريال السعودي إلى هللات (integer)
function toHalalas(amountSar) {
  // نستخدم التقريب لضمان خلو النتيجة من الكسور
  return Math.round(amountSar * 100);
}

// دالة مساعدة: حساب ضريبة القيمة المضافة والمجموع مع الضريبة
function calculateSaudiVAT(subtotalSar) {
  // حساب الضريبة بدقة إلى منزلتين
  const vat = +(subtotalSar * SAUDI_VAT_RATE).toFixed(2); // ضريبة 15%
  const total = +(subtotalSar + vat).toFixed(2);          // الإجمالي مع الضريبة
  return { vat, total };
}

// دوال مساعدة: توليد TLV لرمز QR الخاص بهيئة الزكاة والضريبة (ZATCA)
function tlvEncode(tag, value) {
  // ترميز TLV: [Tag][Length][Value] باستخدام UTF-8
  const valueBytes = Buffer.from(String(value), 'utf8');
  return Buffer.concat([
    Buffer.from([tag]),
    Buffer.from([valueBytes.length]),
    valueBytes
  ]);
}

// توليد رمز QR (Base64) وفق متطلبات ZATCA
function generateZatcaQr({ sellerName, vatNumber, timestampRiyadhISO, totalWithVAT, vatAmount }) {
  const tlvBuffer = Buffer.concat([
    tlvEncode(1, sellerName),                    // اسم المورد
    tlvEncode(2, vatNumber),                     // رقم ضريبة القيمة المضافة
    tlvEncode(3, timestampRiyadhISO),            // التاريخ/الوقت بتوقيت الرياض ISO8601
    tlvEncode(4, totalWithVAT.toFixed(2)),       // إجمالي الفاتورة مع الضريبة
    tlvEncode(5, vatAmount.toFixed(2))           // قيمة الضريبة
  ]);
  return tlvBuffer.toString('base64');
}

/**
 * الدالة الرئيسية: تنفيذ دفعة سعودية عبر Moyasar أو Tap
 * - المدخلات:
 *   gateway: 'moyasar' | 'tap'  // بوابة الدفع
 *   amountSAR: number           // المبلغ قبل الضريبة (بالريال)
 *   description: string         // وصف العملية
 *   paymentSource: string       // رمز دفع Token من الواجهة الأمامية (token/source id)
 *   metadata?: object           // بيانات إضافية
 *   customer?: object           // بيانات العميل (تُستخدم في Tap)
 *   seller?: { name: string, vatNumber: string } // معلومات البائع للفوترة الإلكترونية
 */
export async function processSaudiPayment({
  gateway,
  amountSAR,
  description,
  paymentSource,
  metadata = {},
  customer = {},
  seller = { name: 'متجر سعودي', vatNumber: '300123456700003' }
}) {
  // التحقق من البوابة
  if (!['moyasar', 'tap'].includes(gateway)) {
    throw new Error('بوابة غير مدعومة. استخدم "moyasar" أو "tap".');
  }

  // تثبيت العملة على الريال السعودي
  const currency = 'SAR';

  // حساب الضريبة والإجمالي
  const { vat, total } = calculateSaudiVAT(amountSAR);
  const amountHalalas = toHalalas(total); // بعض بوابات الدفع تتطلب هللات

  // توليد الطابع الزمني بتوقيت الرياض
  const timestampRiyadhISO = DateTime.now().setZone(RIYADH_TZ).toISO();

  let paymentResult;

  if (gateway === 'moyasar') {
    // تحقق من وجود مفتاح Moyasar
    const secret = process.env.MOYASAR_SECRET_KEY;
    if (!secret) throw new Error('MOYASAR_SECRET_KEY مفقود من متغيرات البيئة');

    // ملاحظة أمنية: paymentSource هو token من الواجهة الأمامية (لا ترسل بيانات بطاقات خام إلى الخادم)
    const payload = {
      amount: amountHalalas,     // هللات
      currency,                  // 'SAR'
      description,
      source: { type: 'token', token: paymentSource }, // توكن من Moyasar JS/SDK
      metadata: { ...metadata, vatAmount: vat, subtotal: amountSAR }
    };

    const res = await axios.post('https://api.moyasar.com/v1/payments', payload, {
      auth: { username: secret, password: '' }
    });
    paymentResult = res.data;

  } else if (gateway === 'tap') {
    // تحقق من وجود مفتاح Tap
    const secret = process.env.TAP_SECRET_KEY;
    if (!secret) throw new Error('TAP_SECRET_KEY مفقود من متغيرات البيئة');

    // Tap يستخدم amount بالريال (أي 2 decimal places)
    const payload = {
      amount: +total.toFixed(2), // إجمالي مع الضريبة
      currency,                  // 'SAR'
      threeDSecure: true,
      description,
      customer,                  // { first_name, email, phone, ... }
      source: { id: paymentSource }, // token/source id من Tap JS/SDK
      metadata: { ...metadata, vatAmount: vat, subtotal: amountSAR },
      receipt: { email: true, sms: true } // إرسال إيصال للعميل
    };

    const res = await axios.post('https://api.tap.company/v2/charges', payload, {
      headers: { Authorization: `Bearer ${secret}`, 'Content-Type': 'application/json' }
    });
    paymentResult = res.data;
  }

  // توليد رمز QR متوافق مع ZATCA للفواتير الإلكترونية
  const qrBase64 = generateZatcaQr({
    sellerName: seller.name,
    vatNumber: seller.vatNumber,
    timestampRiyadhISO,
    totalWithVAT: total,
    vatAmount: vat
  });

  // نعيد نتيجة منظمة تحتوي على بيانات الدفع والضريبة والـ QR
  return {
    success: true,
    gateway,
    currency,
    subtotalSAR: amountSAR,
    vatSAR: vat,
    totalSAR: total,
    amountHalalas,
    timestampRiyadhISO,
    zatcaQRBase64: qrBase64,
    raw: paymentResult
  };
}

// مثال استخدام سريع:
/*
(async () => {
  try {
    const result = await processSaudiPayment({
      gateway: 'moyasar',            // أو 'tap'
      amountSAR: 100.00,             // المبلغ قبل الضريبة
      description: 'طلب رقم 1234',
      paymentSource: 'tok_xxxxxx',   // توكن من الواجهة الأمامية
      metadata: { orderId: '1234' },
      customer: {                    // ل Tap (اختياري لـ Moyasar)
        first_name: 'Ahmed',
        email: 'user@example.com',
        phone: { country_code: '966', number: '5xxxxxxxx' }
      },
      seller: {
        name: 'مؤسسة مثال التجارية',
        vatNumber: '310123456700003'
      }
    });
    console.log(result);
  } catch (e) {
    console.error('خطأ في الدفع:', e.message);
  }
})();
*/
