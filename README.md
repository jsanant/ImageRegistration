# ImageRegistration
The Project is mainly focused on image registration of non-rigid images and is to determine an optimal transformation in such 
a way that the transformed template image becomes similar to the reference image as much as possible. To align two test images
after performing operations such as translation, rotation, scaling and shearing for non-rigid objects and identify the maximum 
mutual information between the images. We use pixel based method for the project where first we find the entropy of the image 
then find the histogram, after which we find the joint histogram, then we find the entropy after which we use that to find 
the normalized mutual information.

1. To align two test images after performing operations such as translation for rigid
objects.

2.For non-rigid objects we implement algorithms that learn by themselves and are
able to identify distinct patterns in the images.

