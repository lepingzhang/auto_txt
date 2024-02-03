import requests
from datetime import datetime

hass_url = "http://ip:8123"
access_token = "长期访问令牌"

headers = {
    "Authorization": f"Bearer {access_token}",
    "content-type": "application/json",
}

def get_state(entity_id):
    state_url = f"{hass_url}/api/states/{entity_id}"
    response = requests.get(state_url, headers=headers)
    if response.status_code == 200:
        return response.json()['state']
    else:
        return "未知"

def get_summary():
    try:
        current_date = datetime.now().strftime("%Y年%m月%d日")
        
        boss_plug_status = get_state('switch.qmi_psv3_96ac_switch')
        deng_pc_status = get_state('switch.chuangmi_212a01_fe1a_switch_2')
        drone_charge_status = get_state('switch.chuangmi_212a01_e28f_switch')
        training_charge_status = get_state('switch.chuangmi_212a01_ca9e_switch')
        camera_info = get_state('input_text.she_xiang_tou_tong_ji')
        router_devices = get_state('sensor.192_168_50_1_devices_connected')
        server_status = get_state('sensor.server_status')
        
        try:
            training_plug_statistics = int(get_state('sensor.peixuncp_status'))
        except ValueError:
            training_plug_statistics = "未知"
        
        try:
            total_space = float(get_state('sensor.tya_volume_1_total_size'))
            used_space = float(get_state('sensor.tya_volume_1_used_space'))
            remaining_space = total_space - used_space
        except ValueError:
            total_space = used_space = remaining_space = "未知"
        
        market_power_statuses = {
            '排插': boss_plug_status,
            '电脑': deng_pc_status,
            '充电': drone_charge_status
        }
        if all(status == '未知' for status in market_power_statuses.values()):
            market_description = '所有电源状态未知'
        else:
            market_description = ', '.join([f'{device}插头{status}' if status != '未知' else f'{device}电源状态未知' for device, status in market_power_statuses.items()])
        
        if training_charge_status == '未知' and (training_plug_statistics == '未知' or training_plug_statistics == 0):
            training_description = '所有电源状态未知'
        else:
            training_charge_description = f'训练充电插头{training_charge_status}' if training_charge_status != '未知' else '训练充电插头状态未知'
            training_plug_description = f'排插{training_plug_statistics}个打开' if isinstance(training_plug_statistics, int) and training_plug_statistics > 0 else '排插状态未知'
            training_description = f'{training_charge_description}, {training_plug_description}'
        
        summary = (
            f"今天是{current_date}，公司概况如下：\n\n"
            
            "能源管理：\n"
            f"- 市场部：{market_description}\n"
            f"- 培训部：{training_description}\n\n"
            
            "监控系统：\n"
            f"- 摄像头：{camera_info if camera_info != '未知' else '未获取到画面信息'}\n\n"
            
            "网络核心：\n"
            f"- 路由器：{router_devices if router_devices != '未知' else '在线设备数未知'}个在线设备\n"
            f"- 云服务：{'剩余空间未知' if remaining_space == '未知' else f'剩余空间为{remaining_space:.2f}TB'}\n"
            f"- 服务器：{server_status if server_status != '未知' else '虚拟机数未知'}个虚拟机运行中"
        )
        return summary

    except Exception as e:
        return "生成公司概况信息时发生错误，请检查日志了解详细信息。"

print(get_summary())
