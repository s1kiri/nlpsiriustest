from aiogram import executor
from transformers import AutoModelWithLMHead, AutoTokenizer
import config
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)
context = []
model = AutoModelWithLMHead.from_pretrained(".\model_tune\dialogpt-medium-finetuned")
tokenizer = AutoTokenizer.from_pretrained(".\model_tune\dialogpt-medium-finetuned")
print('ready')
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    global context
    context = []
    await message.answer("Привет! Давай начнем диалог")

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text_message(message: types.Message):
    global context

    user_input = message.text

    if user_input.lower() == 'начать диалог':
        context = []
        await message.answer("Диалог начат! Напиши мне что-то.")

    context.append(f"@@ПЕРВЫЙ@@{user_input}")

    if len(context) > 3:
        context = context[-3:]

    model_input = ''.join(context) + '@@ВТОРОЙ@@'
    print(model_input)
    response = generate_response(model_input)
    
    last_index = response.rfind('@@ВТОРОЙ@@')
    if last_index != -1:
        response = response[last_index + len('@@ВТОРОЙ@@'):]

    context.append(f"@@ВТОРОЙ@@{response}")
    print(context)
    await message.answer(response)

def generate_response(input_text):
    input_text = tokenizer(input_text, return_tensors='pt')

    generated_token_ids = model.generate(
    **input_text,
    top_k=10,
    top_p=0.97,
    num_beams=1,
    num_return_sequences=1,
    do_sample=True,
    no_repeat_ngram_size=2,
    temperature=1.2,
    repetition_penalty=10.1,
    length_penalty=10,
    eos_token_id=50257,
    max_new_tokens=25
    )
    context_with_response = ''.join([tokenizer.decode(token_ids) for token_ids in generated_token_ids])
    print(context_with_response)
    return context_with_response

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
