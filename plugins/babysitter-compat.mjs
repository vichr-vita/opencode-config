const bindSession = (sessionID) => {
  if (!sessionID) return;
  process.env.AGENT_SESSION_ID = sessionID;
  process.env.OPENCODE_SESSION_ID = sessionID;
};

export default async function BabysitterSessionBinding() {
  return {
    event: async ({ event }) => {
      if (event.type === "session.created" || event.type === "session.updated") {
        bindSession(event.properties?.info?.id);
      }
    },
    "chat.message": async ({ sessionID }) => bindSession(sessionID),
    "command.execute.before": async ({ sessionID }) => bindSession(sessionID),
    "tool.execute.before": async ({ sessionID }) => bindSession(sessionID),
  };
}
