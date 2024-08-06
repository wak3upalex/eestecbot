import asyncio

from aiogram import Bot, Dispatcher, types, Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import FSInputFile
import httplib2
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import creds
import logging
import re
from datetime import datetime
from bot import bot, dp

def get_service_sacc():
    creds_json = "kpiinfo-f2eb171a014e.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)
@dp.message(Command(commands=['KPI']))
async def process_KPI_command(message: Message):
    id = str(message.chat.id)
    file = open("users.txt", "r")
    bol = "none"
    for line in file:
        if id in line:
            bol = line
            break
    file.close()
    if (bol != "none"):
        sheet_id = '172rh115qDUxtYUCAroXFqlh-tuZTmS8ifJcYj-EsWGM'
        service = get_service_sacc()
        sheet = service.spreadsheets()
        results = sheet.values().get(spreadsheetId=sheet_id, range="KPI!B3:H91").execute()
        KPI = results['values']
        bol = bol.replace(id + ' ','')
        bol = bol.replace('\n', '')
        # TODO: add text description of the numbers of KPI. Try to refactor it into solo message not a group of messages to avoid message spam
        for i in range(len(KPI)):
            if (len(KPI[i]) !=0):
                if bol[0:bol.rfind(" ")-1] in KPI[i][0]:
                    await bot.send_message(message.chat.id, KPI[i][6])
    else:
        await bot.send_message(message.chat.id, "Для начала пройдите регистрацию")
dp.message.register(process_KPI_command, Command(commands='KPI'))

