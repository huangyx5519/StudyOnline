# -*- coding: utf-8 -*-
from operation.models import UserMessage


def sendMsg(user_id,message,send_id=0):

    user_message = UserMessage()
    user_message.sender=send_id
    user_message.user = user_id
    user_message.message = message
    user_message.save()