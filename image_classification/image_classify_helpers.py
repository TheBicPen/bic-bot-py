
from . import image_classify as ic

tf_sess = None
classifications = None


def start_tf():
    global tf_sess
    global classifications
    classifications = ic.get_classifications()
    if tf_sess is not None:
        print("TensorFlow session already exists")
        return "TensorFlow session already exists"
    tf_sess = ic.main()
    return "started TensorFlow session"


def stop_tf():
    global tf_sess
    global classifications
    tf_sess.close()  # free resources used by the tf session
    tf_sess = None  # remove the reference to it
    classifications = None
    print("ended TensorFlow session")
    return "ended TensorFlow session"


async def classify_attachment(message, tf_sess, classifications):
    if classifications is None:
        return "image classifications not found"
    if tf_sess is None:
        return "TensorFlow session not found"
    if len(message.attachments) == 0:
        return "no valid attachments in message"

    # check image using image-classification
    attachment = message.attachments[0]
    print("message contains attachment at:{0}".format(attachment.url))
    #img = urllib.request.urlretrieve(url)
    # async with aiohttp.get(url) as response:
    #     print(response)
    #     if response.status != 200:
    #         return "unable to retrieve image"
    #     img = await response.read()
    #     print(type(img))
    #     result = ic.classify_image(img, tf_sess, classifications)
    img = await attachment.read()
    result = ic.classify_image(img, tf_sess, classifications)
    return (result, attachment)


async def image_category(message, tf_sess, classifications):
    result = await classify_attachment(message, tf_sess, classifications)
    return "image {2} is {0}. {1:.2f} % confident".format(result[0][0], result[0][1], result[1].filename)


async def image_appropriate(message, tf_sess, classifications, whitelist, blacklist, threshold):
    category = classify_attachment(message, tf_sess, classifications)
    if category[0] not in blacklist and category[0] in whitelist and category[1] > threshold:
        return True
    else:
        return channel_for_cat.get(category[0], message.channel)
