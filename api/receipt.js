// Vercel Serverless — Gemini Vision 영수증 분석 API
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST만 허용됩니다.' });

  const apiKey = process.env.GEMINI_API_KEY;
  const model  = process.env.GEMINI_MODEL || 'gemini-2.0-flash';
  if (!apiKey) return res.status(500).json({ error: 'GEMINI_API_KEY가 설정되지 않았습니다.' });

  const { image, mimeType } = req.body;
  if (!image) return res.status(400).json({ error: 'image(base64) 필드가 필요합니다.' });

  const prompt = `당신은 영수증 OCR 전문가입니다. 이 영수증 이미지를 꼼꼼히 분석하여 아래 JSON 형식으로만 응답해주세요. JSON 외 다른 텍스트는 절대 포함하지 마세요.

{
  "가맹점명": "상호명 (없으면 null)",
  "결제일시": "YYYY-MM-DD HH:MM (없으면 null)",
  "총금액": 숫자만 (원·쉼표 제외, 없으면 null),
  "항목": [
    { "품목명": "상품명", "수량": 숫자, "단가": 숫자, "금액": 숫자 }
  ]
}

주의사항:
- 한글 품목명을 정확하게 인식해주세요
- 금액은 숫자만 입력 (원 기호·쉼표 제외)
- 수량이 표시되지 않은 항목은 수량을 1로 입력
- 단가가 없으면 금액과 동일하게 입력
- 항목이 없으면 빈 배열 [] 반환
- 반드시 유효한 JSON만 반환`;

  try {
    const response = await fetch(
      `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${apiKey}`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          contents: [{
            parts: [
              { text: prompt },
              { inline_data: { mime_type: mimeType || 'image/jpeg', data: image } }
            ]
          }],
          generationConfig: { temperature: 0.1, topP: 0.8 }
        })
      }
    );

    if (!response.ok) {
      const err = await response.json();
      return res.status(response.status).json({ error: err });
    }

    const data = await response.json();
    let raw = data.candidates?.[0]?.content?.parts?.[0]?.text ?? '';
    raw = raw.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();

    try {
      const parsed = JSON.parse(raw);
      return res.status(200).json(parsed);
    } catch {
      return res.status(200).json({ raw });
    }
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
