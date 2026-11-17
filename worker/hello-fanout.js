// Cloudflare Email Routing worker for hello@pickaplugin.com (script: pickaplugin-hello-fanout).
// Incoming mail is forwarded only to the agent inbox. Do not add houstoninvestments@gmail.com back.
export default {
  async email(message, env, ctx) {
    await message.forward("aaronhouston@mail.grokbot.com");
  }
};
