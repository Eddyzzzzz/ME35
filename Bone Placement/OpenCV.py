cv2_image = cv2.cvtColor(np.array(cam.raw_image), cv2.COLOR_RGB2BGR)
b,g,r = cv2.split(cv2_image)
grey = cv2.cvtColor(cv2_image, cv2.COLOR_BGRA2GRAY)
cam.show(grey)  # shows any cv2 image in the same spot on the webpage (third image)
image3 = Image.fromarray(grey)
# display(Image.fromarray(r),Image.fromarray(g),Image.fromarray(b))

#cv.calcHist(images, channels, mask, histSize, ranges[, hist[, accumulate]])
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([cv2_image],[i],None,[256],[0,256])
    plt.plot(histr,color = col)  # add the different histograms to the plot
    plt.xlim([0,256])  # define x axis length (cuts off some of the picture)

arr1 = cv2.threshold(r,150,255,cv2.THRESH_BINARY)
arr2 = cv2.threshold(g,50,255,cv2.THRESH_BINARY)
arr3 = cv2.threshold(b,200,255,cv2.THRESH_BINARY)

slice1 = arr1[1][:80, :]  # First 80 rows of arr1
slice2 = arr2[1][80:160, :]  # Rows 81 to 160 of arr2
slice3 = arr3[1][-80:, :]  # Last 80 rows of arr3

# Concatenate the slices vertically
result = np.vstack((slice1, slice2, slice3))
display(Image.fromarray(result))

plt.imshow(r)  # puts red image in the background
display(plt)  #shows it