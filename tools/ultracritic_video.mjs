// ultracritic video pass — temporal dims via glm-4.6v video_url (day-010)
// Usage: node ultracritic_video.mjs <mp4-path> <prompt-file>
import ZAI from 'z-ai-web-dev-sdk';
import { readFileSync } from 'fs';

const [path, promptFile] = process.argv.slice(2);
const prompt = readFileSync(promptFile, 'utf-8');
const b64 = readFileSync(path).toString('base64');

try {
  const zai = await ZAI.create();
  const messages = [
    {
      role: 'user',
      content: [
        { type: 'text', text: prompt },
        { type: 'video_url', video_url: { url: `data:video/mp4;base64,${b64}` } },
      ],
    },
  ];
  const response = await zai.chat.completions.createVision({
    model: 'glm-4.6v',
    messages,
    thinking: { type: 'disabled' },
  });
  const reply = response.choices?.[0]?.message?.content;
  console.log(reply ?? JSON.stringify(response));
} catch (err) {
  console.error('VIDEO_PASS_FAILED:', err?.message || err);
  process.exit(1);
}
