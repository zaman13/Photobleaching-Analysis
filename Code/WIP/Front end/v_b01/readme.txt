Simp. Th =  If pixel brightness > Simp. Th * Maximum brightness, then the pixel is selected as part of an object. (For simple thresholding only)

Blur order = Kernel size of the median blur filter used to get rid of noisy/hot pixels.

Block size = Image sementation block size for adaptive thresholding. Block size x Block size pixels centered around a target pixel is analyzed to calculate whether the target pixel is part of an object or not. This parameter should be determined based on the size of the object.


