import dlib
from skimage import io
num = 1
ftrain = open('labeled/train(hae).txt', 'w')
while num <= 800:
    # Take the image file name from the command line

    file_name = 'origin/HanHaeDeun/%d.jpg'%num

    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()

    # win = dlib.image_window()


    # Load the image into an array
    image = io.imread(file_name)

    # Run the HOG face detector on the image data.
    # The result will be the bounding boxes of the faces in our image.
    detected_faces = face_detector(image, 1)

    print("I found {} faces in the file {}".format(len(detected_faces), file_name))

    # Open a window on the desktop showing the image
    # win.set_image(image)
    # print(image.shape)
    # Loop through each face we found in the image
    if detected_faces is not None:
        for i, face_rect in enumerate(detected_faces):
            # Detected faces are returned as an object with the coordinates
            # of the top, left, right and bottom edges
            print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
            # print(float(face_rect.right() - face_rect.left()), float(face_rect.bottom() - face_rect.top()))
            cx = float((face_rect.right() + face_rect.left())/2)
            cy = float((face_rect.bottom() + face_rect.top())/2)
            # print(cx, cy)
            # print(cx/image.shape[1], cy / image.shape[0])
            xlen = float((face_rect.right() - face_rect.left())) / float(image.shape[1])
            ylen = float((face_rect.bottom() - face_rect.top())) / float(image.shape[0])
            # print(xlen, ylen)
            f = open('labeled/HanHaeDeun/%d.txt' % num, 'w')
            f.write('10 %.6f %.6f %.6f %.6f' %(cx/image.shape[1], cy/image.shape[0], xlen, ylen))
            ftrain.write('data/HanHaeDeun/%d.jpg\n' % num)
            print(num)
            # Draw a box around each face we found
            # win.add_overlay(face_rect)
    f.close()
    # Wait until the user hits <enter> to close the window
    # dlib.hit_enter_to_continue()
    num +=1
ftrain.close()