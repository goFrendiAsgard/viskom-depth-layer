import cv2.cv as cv
import shutil, os

def cut(disparity, image, threshold):
    for i in range(0, image.height):
        for j in range(0, image.width):
            # keep closer object
            if cv.GetReal2D(disparity,i,j) > threshold:
                cv.Set2D(disparity,i,j,cv.Get2D(image,i,j))

def create_3d_model(left_image_file_name, right_image_file_name, result_folder):
    # create result_folder if not exists
    try:
        os.mkdir(result_folder)
    except:
        shutil.rmtree(result_folder)
        os.mkdir(result_folder)
    
    # loading the stereo pair
    left  = cv.LoadImage(left_image_file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)
    right = cv.LoadImage(right_image_file_name, cv.CV_LOAD_IMAGE_GRAYSCALE)
    
    disparity_left  = cv.CreateMat(left.height, left.width, cv.CV_16S)
    disparity_right = cv.CreateMat(left.height, left.width, cv.CV_16S)
    
    # data structure initialization
    state = cv.CreateStereoGCState(16,2)
    # running the graph-cut algorithm
    cv.FindStereoCorrespondenceGC(left,right,
                              disparity_left,disparity_right,state)
    
    # left layers
    left_layers = {}
    for i in xrange(disparity_left.rows):
        for j in xrange(disparity_left.cols):
            value = disparity_left[i,j]
            if value not in left_layers:
                left_layers[value] = []
            left_layers[value].append([i,j])
    
    # right layers
    right_layers = {}
    for i in xrange(disparity_right.rows):
        for j in xrange(disparity_right.cols):
            value = disparity_right[i,j]
            if value not in right_layers:
                right_layers[value] = []
            right_layers[value].append([i,j])
    
    
    # save objs
    layer_count = len(left_layers)
    layer_index = 1
    for key in left_layers:
        obj = None
        obj = cv.CreateMat(left.height, left.width, cv.CV_8UC4) # define as 4 channel (R,G,B and A)
        for i in xrange(left.height):
            for j in xrange(left.width):
                if [i,j] in left_layers[key]:
                    gray = int(left[i,j])
                    obj[i,j] = [gray,gray,gray,255] #BGRA
                else:
                    if [i,j+key] in right_layers[-key]:
                        gray = int(right[i,j+key])
                        obj[i,j] = [gray,gray,gray,255] #BGRA
                    else:
                        obj[i,j] = [0,0,0,0] #BGRA
        cv.SaveImage(result_folder+'/obj_'+str(key)+'.png', obj)
        # Inform progress to user
        print 'Save Layer '+str(layer_index)+' of '+str(layer_count)+' layers'
        layer_index += 1

    # dump json file
    disparity_values = []
    for key in left_layers:
        disparity_values.append(key)
    disparity_values.sort(reverse=True)
    for i in xrange(len(disparity_values)):
        disparity_values[i] = str(disparity_values[i])
    json = 'var layers = ['+','.join(disparity_values)+']'
    f = open(result_folder+'/obj.js', 'w')
    f.write(json)
    f.close()
    
    # copy html from resource
    shutil.copy('res/index.html.res', result_folder+'/index.html')
    
    # save disparity map
    disp_left_visual = cv.CreateMat(left.height, left.width, cv.CV_8U)
    cv.ConvertScale( disparity_left, disp_left_visual, -16 );
    cv.SaveImage( result_folder+'/disparity_left.pgm', disp_left_visual ); # save the map
    
    disp_right_visual = cv.CreateMat(left.height, left.width, cv.CV_8U)
    cv.ConvertScale( disparity_right, disp_right_visual, 16 );
    cv.SaveImage( result_folder+'/disparity_right.pgm', disp_right_visual ); # save the map
    
    print 'Done ...'

if __name__ == '__main__':
    create_3d_model('scene_l.jpg', 'scene_r.jpg', 'tsukuba')