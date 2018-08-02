import cv2

img = cv2.imread("4.jpg")

# print type(img)
# print img.dtype
# print img.shape

# cv2.imshow("test", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


r = img[:, :, 2]
g = img[:, :, 1]
b = img[:, :, 0]
print r.shape
print g.shape
print b.shape

cv2.imshow("r", r)
cv2.imshow("g", g)
cv2.imshow("b", b)
cv2.waitKey(0)
cv2.destroyAllWindows()