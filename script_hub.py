import os
import re
import subprocess
from plugins import register, Plugin, Event, Reply, ReplyType, logger

class ScriptHandler:
    def __init__(self, script_path):
        self.script_path = script_path
    
    def parse_command(self, query):
        return query.strip().split()

    def run(self, event, args):
        try:
            result = subprocess.run(
                ['python', self.script_path] + args,
                capture_output=True,
                text=True
            )
            return self.handle_output(result)
        except Exception as exc:
            logger.error(f'处理脚本执行出错: {exc}')
            return Reply(ReplyType.TEXT, '处理脚本执行出错')

    def handle_output(self, result):
        if result.returncode == 0:
            return Reply(ReplyType.TEXT, result.stdout.strip() if result.stdout else '脚本执行成功')
        else:
            return Reply(ReplyType.TEXT, result.stderr.strip() if result.stderr else '脚本执行失败')

class AutoQA(ScriptHandler):
    def parse_command(self, query):
        return query.split('整理题库：')[1].strip().split()

    def handle_output(self, result):
        if result.returncode == 0:
            return Reply(ReplyType.TEXT, '已完成，原路径已生成新文件')
        else:
            return Reply(ReplyType.TEXT, '未完成，请检查文件名称是否正确')

class GetHaCamera(ScriptHandler):
    def parse_command(self, query):
        return []

    def handle_output(self, result):
        if result.returncode == 0 and '成功保存截图' in result.stdout:
            image_url = 'http://你的快照保存路径/camera_snapshot.jpg'
            return Reply(ReplyType.IMAGE, image_url)
        else:
            return Reply(ReplyType.TEXT, '保存截图失败')

class GetHaEntity(ScriptHandler):
    def parse_command(self, query):
        return []

@register
class ScriptHub(Plugin):
    name = 'script_hub'

    def __init__(self, config: dict):
        super().__init__(config)
        self.handlers = {
            '整理题库：': AutoQA(os.path.join(os.path.dirname(__file__), 'auto_QA.py')),
            '监控快照': GetHaCamera(os.path.join(os.path.dirname(__file__), 'get_ha_camera.py')),
            '房屋概况': GetHaEntity(os.path.join(os.path.dirname(__file__), 'get_ha_entity.py'))
        }

    def did_receive_message(self, event: Event):
        query = event.message.content.strip()
        is_group = event.message.is_group
        if is_group:
            query = re.sub(r'@[\w]+\s+', '', query, count=1).strip()

        for cmd, handler in self.handlers.items():
            if cmd.endswith('：') and query.startswith(cmd):
                args = handler.parse_command(query)
                event.reply = handler.run(event, args)
                event.bypass()
                return
            elif not cmd.endswith('：') and re.match(f"^{cmd}( |$)", query):
                args = handler.parse_command(query)
                event.reply = handler.run(event, args)
                event.bypass()
                return

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
