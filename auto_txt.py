import os
import subprocess
from plugins import register, Plugin, Event, Reply, ReplyType, logger
import re

@register
class AutoTxt(Plugin):
    name = 'auto_txt'

    def __init__(self, config: dict):
        super().__init__(config)

    @property
    def commands(self):
        cmds = self.config.get('command', ['处理文本：', '整理文本：'])
        if not isinstance(cmds, list):
            cmds = [cmds]
        return [cmd.lower() for cmd in cmds]

    def config_for(self, event: Event, key, default=None):
        val = self.config.get(key, {})
        if isinstance(val, dict):
            msg = event.message
            dfl = val.get('*', default)
            val = val.get(msg.room_id or msg.sender_id, dfl)
        return val

    def did_receive_message(self, event: Event):
        query = event.message.content.strip().lower()
        is_group = event.message.is_group
        if is_group:
            query = re.sub(r'@[\w]+\s+', '', query, count=1).strip()

        for cmd in self.commands:
            if query.startswith(cmd):
                filename = query.split(cmd, 1)[1].strip()
                event.reply = self.process_file(event, filename)
                event.bypass()
                return

    def process_file(self, event: Event, filename: str) -> Reply:
        input_file_path = os.path.join(self.config['script_path'], f'{filename}.txt')
        output_dir_path = self.config['script_path']
        script_name = self.config['script_name']
        script_path = os.path.join(self.config['script_path'], script_name)

        if not os.path.exists(input_file_path):
            return Reply(ReplyType.TEXT, '未找到该文件，请确认名称是否正确')

        try:
            result = subprocess.run(
                ['python', script_path, input_file_path, output_dir_path],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                return Reply(ReplyType.TEXT, '文件处理成功，请刷新原路径')
            else:
                return Reply(ReplyType.TEXT, '文件处理失败')
        except Exception as exc:
            return Reply(ReplyType.TEXT, '处理脚本执行出错')

    def help(self, **kwargs):
        return '自动文本处理插件：根据文件名处理文本并保存结果'

    def will_decorate_reply(self, event: Event):
        pass

    def will_send_reply(self, event: Event):
        pass

    def will_generate_reply(self, event: Event):
        pass
