"""
channel factory
"""


def create_channel(channel_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    if channel_type == "terminal":
        from channel.terminal.terminal_channel import TerminalChannel

        return TerminalChannel()
    elif channel_type == "wework":
        from channel.wework.wework_channel import WeworkChannel

        return WeworkChannel()
    elif channel_type == "ntchat":
        from channel.wechatnt.ntchat_channel import NtchatChannel

        return NtchatChannel()
    elif channel_type == "wcferry":
        from channel.wcferry.wcferry_channel import WcFerryChannel

        return WcFerryChannel()
    elif channel_type == "web":
        from channel.web.web_channel import WebChannel

        return WebChannel()
    elif channel_type == "wechatmp":
        from channel.wechatmp.wechatmp_channel import WechatMPChannel

        return WechatMPChannel(passive_reply=True)
    elif channel_type == "wechatmp_service":
        from channel.wechatmp.wechatmp_channel import WechatMPChannel

        return WechatMPChannel(passive_reply=False)
    elif channel_type == "weworktop":
        from channel.weworktop.weworktop_channel import WeworkTopChannel

        return WeworkTopChannel()
    raise RuntimeError
