# from tools.log_analyzer import analyze_uipath_logs

# result = analyze_uipath_logs(
#     "C:\\Users\AnkushAnkush2\\Desktop\\agentic_rpa_bot_analyzer\\data\\sample_logs\\robot_logs.csv"
# )

# print(result)

from agent.controller import RPABotFailureAgent

agent = RPABotFailureAgent(
    log_path="C:\\Users\AnkushAnkush2\\Desktop\\agentic_rpa_bot_analyzer\\data\\sample_logs\\robot_logs.csv"
)

output = agent.run()
print(output)

