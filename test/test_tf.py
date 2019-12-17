from image_classification import image_classify as ic

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
    img = await attachment.read()
    result = ic.classify_image(img, tf_sess, classifications)
    return (result, attachment)
