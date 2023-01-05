import os
import asyncio
import logging
import json
from aio_pika import Message, connect
from aio_pika.abc import AbstractIncomingMessage

import torch
from torch.autograd import Variable
from torchvision.utils import save_image
from PIL import Image
from models import TransformerNet
from utils import *

def style_image(content_path, name):
    device = torch.device("cpu")

    transform = style_transform()

    # Определение модели, загрузка весов модели 
    transformer = TransformerNet().to(device)
    transformer.load_state_dict(torch.load(content_path))
    transformer.eval()

    # Загрузка контентного изображения
    image_tensor = Variable(transform(Image.open('/app/photo/content_image' + str(name) + '.jpg'))).to(device)
    image_tensor = image_tensor.unsqueeze(0)
    
    # Стилизация изображения
    with torch.no_grad():
        stylized_image = denormalize(transformer(image_tensor)).cpu()
        
    # Сохранение сгенерированного изображения
    save_image(stylized_image, f"/app/photo/stylized_image" + str(name) + ".jpg")

logging.basicConfig(level = logging.INFO)

async def main() -> None:
    try:
        connection = await connect(os.environ["AMQP_URL"],)
    except Exception:
        logging.exception("connection not open")

    channel = await connection.channel()

    exchange = channel.default_exchange

    queue = await channel.declare_queue("rpc_queue", durable = True)

    logging.info(" [x] Awaiting RPC requests")

    async with queue.iterator() as qiterator:
        message: AbstractIncomingMessage
        async for message in qiterator:
            try:
                async with message.process(requeue = True):
                    assert message.reply_to is not None
                    inputJson = message.body.decode("UTF-8")
                    print(inputJson)
                    inputMessage = json.loads(inputJson)
                    print(inputMessage['text'], inputMessage['user_id'])
                    style_image(inputMessage['text'], inputMessage['user_id'])
                    outputText = inputMessage['user_id']
                    logging.info("Output text: %r", outputText)
                    outputText = inputMessage['text']
                    inputMessage['text'] = outputText
                    outputJson = json.dumps(inputMessage)
                    response = outputJson.encode("UTF-8")
                    await exchange.publish(
                        Message(
                            body = response,
                            correlation_id = message.correlation_id,
                        ),
                        routing_key = message.reply_to,
                    )

            except Exception:
                logging.exception("Processing error for message %r", message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info(" [x] Server is down")
