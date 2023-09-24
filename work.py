
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

import BCH_add , thingsForBot
TOKEN = '6543892179:AAFfRcjL16mxQtwbKKeMe9765RYZxvjOWCQ'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

global allow_array_user
allow_array_user = ['953288255','748305413','822841237']

@dp.message_handler(commands=['start'])
async def on_start(message: types.Message):
    global array_user
    if str(message.chat.id) in allow_array_user:
     markup = types.InlineKeyboardMarkup(row_width = 1)
     btn1 = types.InlineKeyboardButton("Make new block", callback_data= f"createNewBlock")
     btn2 = types.InlineKeyboardButton("Add transaction", callback_data= f"addTransaction")
     btn3 = types.InlineKeyboardButton("Show blockchain", callback_data= f"showBlockchain")
     btn4 = types.InlineKeyboardButton("Check blocks", callback_data= f"checkBlocks")
     if str(message.chat.id) == '953288255':
             markup.add(btn1, btn2,btn3,btn4)
     else:
             markup.add( btn2,btn3,btn4) 
     await bot.send_message(message.chat.id, text='Welcome to the our Blockchain Bot!\nWhat you want?', reply_markup=markup)

my_blockchain = BCH_add.Blockchain()
@dp.callback_query_handler()
async def callback_function(call: types.CallbackQuery , state:FSMContext):
    global array_user
    if str(call.message.chat.id) in allow_array_user:
        try:
         await call.message.delete()
        except:
         pass
        if call.data.startswith("createNewBlock"):
        #    await bot.send_message(call.message.chat.id, text='Wait pls I am creating')           
           if my_blockchain.add_block("General Block") :
              await bot.send_message(call.message.chat.id, text='Your block uspeshno created!')
           else:
              await bot.send_message(call.message.chat.id, text='Your block destricted!')
         
           markup = types.InlineKeyboardMarkup(row_width = 1)
           btn1 = types.InlineKeyboardButton("Make new block", callback_data= f"createNewBlock")
           btn2 = types.InlineKeyboardButton("Add transaction", callback_data= f"addTransaction")
           btn3 = types.InlineKeyboardButton("Show blockchain", callback_data= f"showBlockchain")
           btn4 = types.InlineKeyboardButton("Check blocks", callback_data= f"checkBlocks")
           if str(call.message.chat.id) == '953288255':
             markup.add(btn1, btn2,btn3,btn4)
           else:
             markup.add( btn2,btn3,btn4)
           await bot.send_message(call.message.chat.id, text='What you want?', reply_markup=markup)
              
        #    тут функцияны шакырамз
        elif call.data.startswith("addTransaction"):
         markup = types.InlineKeyboardMarkup(row_width = 1)
         btn1 = types.InlineKeyboardButton("Ayazhan", callback_data= f"recipient/Ayazhan")
         btn2 = types.InlineKeyboardButton("Meruert", callback_data= f"recipient/Meruert")
         btn3 = types.InlineKeyboardButton("Aigerim", callback_data= f"recipient/Aigerim")
         if str(call.message.chat.id) == '953288255':
            await state.update_data(sender = "Aigerim")
            markup.add(btn1, btn2) 
            await bot.send_message(call.message.chat.id, text='Aigerim, choose recipient:', reply_markup=markup)
         elif str(call.message.chat.id) == '748305413':
            await state.update_data(sender = "Ayazhan")
            markup.add(btn2, btn3)
            await bot.send_message(call.message.chat.id, text='Ayazhan, choose recipient:', reply_markup=markup)
         elif str(call.message.chat.id) == '822841237':
            await state.update_data(sender = "Meruert")
            markup.add(btn3, btn1)
            await bot.send_message(call.message.chat.id, text='Meruert, choose recipient:', reply_markup=markup)
         
        #    тут функция 
        elif call.data.startswith("showBlockchain"):
            for block in my_blockchain.chain:
                msg = f"Block - Index #{block.index}\n"
                msg +=f"Data: {block.data}\n"
                msg+=f"Timestamp: {block.timestamp}\n"
                msg +=f"Previous Hash: {block.previous_hash}\n"
                msg+="Transactions:\n"
                for transaction in block.transactions:
                  try:
                    msg+=f"{str(transaction.to_string())}\n"        
                  except:
                     msg+=f"{str(transaction)}\n"  
                  msg+="--------------\n"        
                msg+= f"Hash: {block.hash}\n"
                if isinstance(block.merkle_hash, int):
                    msg += f"Merkle Hash: {block.merkle_hash}\n"
                else:
                    msg += f"Merkle Hash: {block.merkle_hash[0]}\n"
                # msg +=f"Merkle Hash: {block.merkle_hash.to_string()}\n"
                await bot.send_message(call.message.chat.id, text=msg)
            markup = types.InlineKeyboardMarkup(row_width = 1)
            btn1 = types.InlineKeyboardButton("Make new block", callback_data= f"createNewBlock")
            btn2 = types.InlineKeyboardButton("Add transaction", callback_data= f"addTransaction")
            btn3 = types.InlineKeyboardButton("Show blockchain", callback_data= f"showBlockchain")
            btn4 = types.InlineKeyboardButton("Check blocks", callback_data= f"checkBlocks")
            if str(call.message.chat.id) == '953288255':
             markup.add(btn1, btn2,btn3,btn4)
            else:
             markup.add( btn2,btn3,btn4)
            await bot.send_message(call.message.chat.id, text='What you want?', reply_markup=markup)

        elif call.data.startswith("recipient/"):
           print(call.data.split("/")[-1])
           await state.update_data(recipient = call.data.split("/")[-1])
           await bot.send_message(call.message.chat.id, text="How much you want to send?")
           await thingsForBot.Questionnaire().howMuchCoins.set()
        elif call.data.startswith("checkBlocks"):
           if  my_blockchain.checkBlocks_valid() is True:
              await bot.send_message(call.message.chat.id, text='Bloktarmen bari duryc')
           elif my_blockchain.checkBlocks_valid() is False:
              await bot.send_message(call.message.chat.id, text='Kurygan zherimiz osy!')
           elif my_blockchain.checkBlocks_valid() == 'genesis':
              await bot.send_message(call.message.chat.id, text='You dont have working blocks!')
           markup = types.InlineKeyboardMarkup(row_width = 1)
           btn1 = types.InlineKeyboardButton("Make new block", callback_data= f"createNewBlock")
           btn2 = types.InlineKeyboardButton("Add transaction", callback_data= f"addTransaction")
           btn3 = types.InlineKeyboardButton("Show blockchain", callback_data= f"showBlockchain")
           btn4 = types.InlineKeyboardButton("Check blocks", callback_data= f"checkBlocks")
           if str(call.message.chat.id) == '953288255':
             markup.add(btn1, btn2,btn3,btn4)
           else:
             markup.add( btn2,btn3,btn4)
           await bot.send_message(call.message.chat.id, text='What you want?', reply_markup=markup)
              
           

@dp.message_handler(state=thingsForBot.Questionnaire().howMuchCoins, content_types=[ types.ContentType.TEXT] )
async def handle_question1(message: types.Message, state: FSMContext):
  if message.text :
      await state.update_data(send_coins =message.text )
      print(message.text)
      await bot.send_message(message.chat.id, text="Your message:")
      await thingsForBot.Questionnaire().Message_ToSend.set()

 
@dp.message_handler(state=thingsForBot.Questionnaire().Message_ToSend, content_types=[ types.ContentType.TEXT] )
async def handle_question1(message: types.Message, state: FSMContext):
  if message.text :
      await state.update_data(send_message =message.text )
      user_data = await state.get_data()
      sender = user_data['sender']
      coins = user_data['send_coins']
      print(message.text)
      new_transaction = BCH_add.callforTransactionStructure(user_data['sender'], user_data['recipient'], user_data['send_coins'] , message.text)
      await state.finish()
      my_blockchain.update_list_transactions(new_transaction)
      if my_blockchain.addTransaction() is True:#updatecurrentBlock
        if user_data['recipient'] =="Aigerim":
         await bot.send_message(953288255, text=f"Miss. {sender} send {coins} coins.\n Message from {sender}:\n{message.text}")
        elif  user_data['recipient'] =="Ayazhan":
         await bot.send_message(748305413, text=f"Miss. {sender} send {coins} coins.\n Message from {sender}:\n{message.text}")
        elif  user_data['recipient'] =="Meruert":
         await bot.send_message(822841237, text=f"Miss. {sender} send {coins} coins.\n Message from {sender}:\n{message.text}")
        
        await bot.send_message(message.chat.id, text="Your transaction succesfuli finished!")

      elif str(my_blockchain.addTransaction())=='genesis':#updatecurrentBlock
        await bot.send_message(message.chat.id, text="Please create block before adding transactions.")
      else:
        await bot.send_message(message.chat.id, text="Your transaction invalid bolyp qaldy!")
      markup = types.InlineKeyboardMarkup(row_width = 1)
      btn1 = types.InlineKeyboardButton("Make new block", callback_data= f"createNewBlock")
      btn2 = types.InlineKeyboardButton("Add transaction", callback_data= f"addTransaction")
      btn3 = types.InlineKeyboardButton("Show blockchain", callback_data= f"showBlockchain")
      btn4 = types.InlineKeyboardButton("Check blocks", callback_data= f"checkBlocks")

      if str(message.chat.id) == '953288255':
        markup.add(btn1, btn2,btn3,btn4)
      else:
        markup.add( btn2,btn3,btn4)
      await bot.send_message(message.chat.id, text='What you want?', reply_markup=markup)
 
executor.start_polling(dp, skip_updates=True)
