from SolveLinear3 import solve_linear_3

COEFFICIENTS_FOR_THIRD_EQUATION = [1,1,1] # required for the function
                                          # is_point_inside_triangle

ANSWER_TO_THIRD_EQUATION = 1 # required for the function
                             # is_point_inside_triangle

NUMBER_OF_SMALL_TRIANGLES_PER_SPLIT = 3 # the number of triangles each big
                                        # triangle is split into in function
                                        # create_triangles

POINTS_GIVEN_AT_THE_START = 4  # amount of points on the screen when gui.py
                               # is opened

INDEX_OF_X_COORDINATE = 0
INDEX_OF_Y_COORDINATE = 1

INDEX_OF_RED_IN_RGB = 0
INDEX_OF_GREEN_IN_RGB = 1
INDEX_OF_BLUE_IN_RGB = 2

INDEX_OF_FIRST_TRIANGLE_EDGE = 0
INDEX_OF_SECOND_TRIANGLE_EDGE = 1
INDEX_OF_THIRD_TRIANGLE_EDGE = 2



def is_point_inside_triangle(point, v1, v2, v3):

    '''This function receives a point and three corners of a triangle (each of
     these is represented as a tuple of the (x,y) coordinates) and checks if
     the point is inside the triangle. Returns a Tuple in which the first item
     is True or False, according to the result of the function, and a tuple 
	 containing the numbers of a,b,c that are received from the equations
	 used '''

    # Calculating the following equations - with px py being the coordinates
    # of the point, and v1x,v1y being the coordinates of the first corner of
	# the triangle (and the same for the others) -  in order to find a,b,c:
    # v1x*a + v2x*b + v3x*c = px
    # v1y*a + v2y*b + v3y*c = py
    # a + b +c = 1
    # (Solving the equation using the function solve_linear_3)


    x_coordinates_of_corners = [v1[INDEX_OF_X_COORDINATE],\
                       v2[INDEX_OF_X_COORDINATE],v3[INDEX_OF_X_COORDINATE]]
    y_coordinates_of_corners = [v1[INDEX_OF_Y_COORDINATE],\
                        v2[INDEX_OF_Y_COORDINATE],v3[INDEX_OF_Y_COORDINATE]]
    right_hand_list = [point[INDEX_OF_X_COORDINATE],\
                        point[INDEX_OF_Y_COORDINATE],ANSWER_TO_THIRD_EQUATION]



    equations_answers = solve_linear_3([x_coordinates_of_corners,\
                   y_coordinates_of_corners,COEFFICIENTS_FOR_THIRD_EQUATION]\
                                                    ,right_hand_list)



    a,b,c = equations_answers


    # If a,b, and c are between 0 and 1, the point is in the triangle.
    # Since a + b + c = 1, the program will see if any of them are smaller
    # than 0. If not, they are all in between 0 and 1 and the point is in the
    # triangle.

    if a < 0 or b < 0 or c < 0:
        is_in_triangle = False
    else:
        is_in_triangle = True

    return is_in_triangle,equations_answers



def create_triangles(list_of_points):
    '''This function receives the list of points selected on an image and
    returns a list of triangles (each triangle represented by a tuple which
    has three point, and each of these points is another tuple with the the
    two coordinates of x,y). The function will first split the screen into
    two triangle using the four corner points (defined to be the first points 
    in the given list) and then for every next point in the list will check 
    what triangle it fits into (out of the triangles previously created in
    the function) and delete that triangle from the created list, replacing
    it with three new triangles created by the new point within the big
    triangle.'''

    # Creating a list with two big triangles, using the corner points.
    # (the program will always start with the first and second points on the
    # top and the other two on the bottom, two and three on the right side
    # and the rest on the left, so the split 0,1,2 - 0,2,3 will create two
    # triangle)

    triangles_list = [(list_of_points[0],list_of_points[1],list_of_points[2])
                ,(list_of_points[0],list_of_points[2],list_of_points[3])]

	# Spliting for each point a big triangle into 3 small ones, starting from
	# the fifth point.

    for point in list_of_points[POINTS_GIVEN_AT_THE_START:]:

        for triangle_index in range(len(triangles_list)):

            if is_point_inside_triangle(point,\
                        triangles_list[triangle_index]\
                           [INDEX_OF_FIRST_TRIANGLE_EDGE],\
                               triangles_list[triangle_index]\
                                  [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                                   triangles_list[triangle_index]\
                                           [INDEX_OF_THIRD_TRIANGLE_EDGE])[0]:

                removed_triangle = triangles_list.pop(triangle_index)
                for i in range(NUMBER_OF_SMALL_TRIANGLES_PER_SPLIT):
                    # inserting three new triangles, each with the given point
                    # and two of the old triangle's edges (using modulu so all
                    # edges can be used within the loop)
                    triangles_list.insert(triangle_index + i,\
                                       (point,removed_triangle[i],\
                                         removed_triangle[(i+1) %\
                                        NUMBER_OF_SMALL_TRIANGLES_PER_SPLIT]))

                break

    return triangles_list





def do_triangle_lists_match(list_of_points1, list_of_points2):
    '''This function gets two lists of points, and builds two corresponding
    lists of triangles using the function create_triangles. It then checks if
    every two points with the same index in the two lists are each inside a
    triangle that has the same index of the other. Returns true or false
    accordingly'''

    triangles_list1 = create_triangles(list_of_points1)
    triangles_list2 = create_triangles(list_of_points2)

    for i in range(len(list_of_points1)):
        for j in range(len(triangles_list1)):
            if is_point_inside_triangle(list_of_points1[i],triangles_list1[j]\
                       [INDEX_OF_FIRST_TRIANGLE_EDGE],\
                           triangles_list1[j][INDEX_OF_SECOND_TRIANGLE_EDGE],\
                                    triangles_list1[j]\
                                         [INDEX_OF_THIRD_TRIANGLE_EDGE])[0]:

            # If a point is found in one triangle and not in the other, the
            # test fails and there is no need to keep checking. 

                if not is_point_inside_triangle(list_of_points2[i],\
                           triangles_list2[j]\
                               [INDEX_OF_FIRST_TRIANGLE_EDGE],
                                   triangles_list2[j]\
                                      [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                                         triangles_list2[j]\
                                           [INDEX_OF_THIRD_TRIANGLE_EDGE])[0]:
                    return False

    return True





def get_point_in_segment(p1, p2, alpha):
    '''This function receives two points and a number between 1-0 (alpha).
    it returns a point which is at the distance of alpha from p1 and at the
    distance of 1-alpha from p2. Meaning the point is "on the way" from
    p1 to p2 and advanced alpha steps so far. The given tuple is returned
    as a tuple of coordinates, x and y'''

    x_of_new_point = (1-alpha)*p1[INDEX_OF_X_COORDINATE]\
                                       + alpha*p2[INDEX_OF_X_COORDINATE]
    y_of_new_point = (1-alpha)*p1[INDEX_OF_Y_COORDINATE]\
                                       + alpha*p2[INDEX_OF_Y_COORDINATE]

    return x_of_new_point, y_of_new_point





def get_intermediate_triangles(source_triangles_list, target_triangles_list,
                                                                  alpha):
    '''This function receives two lists of triangles and a number from 0 to 1
    (alpha). It returns a list of triangles, each triangle a distance of
    alpha from its corresponding triangle in the source list, and a distance
    of 1-alpha from its corresponding triangle in the target list. So each
    triangle is "on the way" from a source triangle to a target triangle.
    The function uses the function get_point_in_segment, which does the
    same operation for points, and uses it for each edge of the triangles'''

    triangles_list = []

    for i in range(len(source_triangles_list)):

        current_triangle_edge_1 =  get_point_in_segment\
            (source_triangles_list[i][INDEX_OF_FIRST_TRIANGLE_EDGE]\
                ,target_triangles_list[i][INDEX_OF_FIRST_TRIANGLE_EDGE],alpha)

        current_triangle_edge_2 =  get_point_in_segment\
            (source_triangles_list[i][INDEX_OF_SECOND_TRIANGLE_EDGE]\
               ,target_triangles_list[i][INDEX_OF_SECOND_TRIANGLE_EDGE],alpha)

        current_triangle_edge_3 =  get_point_in_segment\
            (source_triangles_list[i][INDEX_OF_THIRD_TRIANGLE_EDGE]\
                ,target_triangles_list[i][INDEX_OF_THIRD_TRIANGLE_EDGE],alpha)


        triangles_list.append((current_triangle_edge_1,\
                             current_triangle_edge_2,current_triangle_edge_3))

    return triangles_list






def get_array_of_matching_points(size,triangles_list,
                                 intermediate_triangles_list):
    '''This function receives the size of a screen (in a tuple of pixel rows
    times pixel columns), gets the triangle list of the source or target image
    and gets the triangle list of the intermediate image created in between
    the source and target image. The function takes each pixel from the
    intermediate image and finds what triangle (out of the intermediate
    triangles list) it belongs to. Then it finds the corresponding triangle
    in the source/target triangles list that was given (according to its
    index) and finds the corresponding pixel in the source/target image
    according to the function find_matching_pixel_in_original_triangle.
    The function returns the pixels that were found as a list of lists
    of the given size of the screen, with each item in the sub-list
    being a tuple of the found pixel's coordinates'''


    # Variable for saving the previously found triangle, as there is a good
    # chance that the next pixel will be in it as well. Starting at 0 as
    # default, the first run will check if the pixel fits the first triangle
    # and if not will keep on checking.

    current_triangle_index = 0

    list_of_matching_pixels = []




    for x in range(size[INDEX_OF_X_COORDINATE]):
        column_list_of_matching_pixels = [] # Will be the sub-list
        for y in range(size[INDEX_OF_Y_COORDINATE]):

            is_point_inside_test = is_point_inside_triangle((x,y),\
               intermediate_triangles_list[current_triangle_index]\
                    [INDEX_OF_FIRST_TRIANGLE_EDGE],
                      intermediate_triangles_list[current_triangle_index]\
                        [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                          intermediate_triangles_list[current_triangle_index]\
                              [INDEX_OF_THIRD_TRIANGLE_EDGE])

            if is_point_inside_test[0]:
                #If the point is in the current triangle (from the previous
                # iteration), the relevant pixel is appended and we move on 
                # stright to the next iteration (the next y coordinate)

                column_list_of_matching_pixels.append\
                  (find_matching_pixel_in_original_triangle\
                     (triangles_list[current_triangle_index],\
                       is_point_inside_test[1]\
                         [INDEX_OF_FIRST_TRIANGLE_EDGE],\
                          is_point_inside_test[1]\
                            [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                               is_point_inside_test[1]\
                                  [INDEX_OF_THIRD_TRIANGLE_EDGE]))
                
                
                continue
            

            else:

                #Check if the point is in the other triangles
                for i in range(len(triangles_list)):

                    # Skipping over the current triangle index that was
                    # already checked
                    if i != current_triangle_index:

                        is_point_inside_test = is_point_inside_triangle((x,y)\
                                  ,intermediate_triangles_list[i]\
                                     [INDEX_OF_FIRST_TRIANGLE_EDGE],
                                       intermediate_triangles_list[i]\
                                          [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                                             intermediate_triangles_list[i]\
                                               [INDEX_OF_THIRD_TRIANGLE_EDGE])

                        if is_point_inside_test[0]:
                            column_list_of_matching_pixels.append\
                                    (find_matching_pixel_in_original_triangle\
                                      (triangles_list[i],\
                                        is_point_inside_test[1]\
                                         [INDEX_OF_FIRST_TRIANGLE_EDGE],\
                                          is_point_inside_test[1]\
                                           [INDEX_OF_SECOND_TRIANGLE_EDGE],\
                                             is_point_inside_test[1]\
                                              [INDEX_OF_THIRD_TRIANGLE_EDGE]))
                            #If triangle is found, move on to next iteration                            
                            break

        #Appending the sublist of columns to the list of rows
        list_of_matching_pixels.append(column_list_of_matching_pixels)


    return list_of_matching_pixels




def find_matching_pixel_in_original_triangle(original_triangle,a,b,c):
    '''This function receives an triangle in the original image (the source
    or the target) and the a,b,c that are the result of the
    is_point_inside_triangle function which was used by the function 
    get_array_of_matching_points on an intermediate pixel.
    The function finds the pixel in the original triangle that matches the
    intermediate pixel using the following equation and returns it as a
    tuple:
    x = a*v1x + b*v2x + c*v3x
    y = a*v1y + b*v2y + c*v3y
    (with a,b,c being the result of the is_point_inside_triangle function and
    v1x,v1y and so forth being the coordinates of the corners of the
    relevant triangle in the source/target list.)'''

    x = a*original_triangle[INDEX_OF_FIRST_TRIANGLE_EDGE]\
                                               [INDEX_OF_X_COORDINATE] +\
                  b*original_triangle[INDEX_OF_SECOND_TRIANGLE_EDGE]\
                                               [INDEX_OF_X_COORDINATE]+\
                         c*original_triangle[INDEX_OF_THIRD_TRIANGLE_EDGE]\
                                               [INDEX_OF_X_COORDINATE]

    y = a*original_triangle[INDEX_OF_FIRST_TRIANGLE_EDGE]\
                                               [INDEX_OF_Y_COORDINATE] +\
                  b*original_triangle[INDEX_OF_SECOND_TRIANGLE_EDGE]\
                                               [INDEX_OF_Y_COORDINATE]+\
                         c*original_triangle[INDEX_OF_THIRD_TRIANGLE_EDGE]\
                                               [INDEX_OF_Y_COORDINATE]
    return x,y



def create_intermediate_image(alpha, size, source_image, target_image,
                              source_triangles_list, target_triangles_list):
    '''This function recives an alpha (degree of change from the source to the
    target image), the size of the screen, the source and target images,
    and the source and target lists of created triangles. It returns a lists
    of lists at the size of the screen representing an intermediate image 
    which is alpha "on the way" to the target. The list of lists 
    contains a tuple of the RGB of each pixel. Each pixel is matched to a 
    a pixel at the source and a pixel at the target 
    (using get_array_of_matching_points for both source and target) and each 
    RGB is the calculated as being alpha "on the way" from the matched source
    pixel to the matched target pixel'''



    intermediate_image = []

    intermediate_triangles_list = get_intermediate_triangles(
        source_triangles_list,target_triangles_list,alpha)

    source_matching_points = get_array_of_matching_points(size,\
                            source_triangles_list,intermediate_triangles_list)

    target_matching_points = get_array_of_matching_points(size,\
                            target_triangles_list,intermediate_triangles_list)

    for i in range(size[INDEX_OF_X_COORDINATE]):
        column_list_of_intermediate_image = [] # Will be the sub-list
        for j in range(size[INDEX_OF_Y_COORDINATE]):
      
            pixel_of_current_source_point = source_image\
                 [source_matching_points[i][j][INDEX_OF_X_COORDINATE]\
                         ,source_matching_points[i][j][INDEX_OF_Y_COORDINATE]]

            pixel_of_current_target_point = target_image\
                 [target_matching_points[i][j][INDEX_OF_X_COORDINATE]\
                         ,target_matching_points[i][j][INDEX_OF_Y_COORDINATE]]
               

            red = (1 - alpha)*pixel_of_current_source_point\
                                  [INDEX_OF_RED_IN_RGB] + \
                                        alpha*pixel_of_current_target_point\
                                               [INDEX_OF_RED_IN_RGB]

            green = (1 - alpha)*pixel_of_current_source_point\
                                  [INDEX_OF_GREEN_IN_RGB] + \
                                        alpha*pixel_of_current_target_point\
                                               [INDEX_OF_GREEN_IN_RGB]

            blue = (1 - alpha)*pixel_of_current_source_point\
                                  [INDEX_OF_BLUE_IN_RGB] + \
                                        alpha*pixel_of_current_target_point\
                                               [INDEX_OF_BLUE_IN_RGB]

            # Turning the RGB into ints since the calculations above make 
            # them floats.
            column_list_of_intermediate_image.append((int(red),int(green),
                                                   int(blue)))
         
        #Appending the sublist of columns to the list of rows
        intermediate_image.append(column_list_of_intermediate_image)

    return intermediate_image









def create_sequence_of_images(size, source_image, target_image, 
                source_triangles_list, target_triangles_list, num_frames):
    '''This function the size of the screen, the source and target images,
    the source and target lists of created triangles, and the number or 
    intermediate frames to be created. It uses create_intermediate_image
    to make each frame and returns a list of all the frames. For each frame
    number, the relevant alpha is calulated as
     - current_frame_number / (total_number_of_frames -1)'''

    frames_list = []
    for i in range(num_frames):
        alpha = i / (num_frames-1)

        frames_list.append(create_intermediate_image(alpha,size,
                                                     source_image,
                                                     target_image,
                                                     source_triangles_list,
                                                     target_triangles_list))


    return frames_list






