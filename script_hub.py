import os
import subprocess
from plugins import register, Plugin, Event, Reply, ReplyType, logger
import re

@register
class ScriptHub(Plugin):
    name = 'script_hub'

    def __init__(self, config: dict):
        super().__init__(config)

    @property
    def commands(self):
        return self.config.get('commands', {})

    def did_receive_message(self, event: Event):
        query = event.message.content.strip().lower()
        is_group = event.message.is_group
        if is_group:
            query = re.sub(r'@[\w]+\s+', '', query, count=1).strip()

        for cmd, script_name in self.commands.items():
            if query.startswith(cmd.lower()):
                filename = query.split(cmd, 1)[1].strip()

                event.reply = self.process_script(event, filename, script_name)
                event.bypass()
                return

    def process_script(self, event: Event, filename: str, script_name: str) -> Reply:
        script_path = os.path.join(os.path.dirname(__file__), script_name)

        try:
            result = subprocess.run(
                ['python', script_path, filename],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                success_message = result.stdout if result.stdout else '文件处理成功'
                return Reply(ReplyType.TEXT, success_message)
            else:
                error_message = result.stderr if result.stderr else '文件处理失败'
                return Reply(ReplyType.TEXT, error_message)
        except Exception as exc:
            return Reply(ReplyType.TEXT, '处理脚本执行出错')

    def help(self, **kwargs):
        return '根据关键词调用不同的脚本执行任务'

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        pass

if __name__ == "__main__":
    main()
