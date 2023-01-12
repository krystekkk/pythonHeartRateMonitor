import numpy as np
import cv2

sOutFileName = "pulse.txt"
outFile = open(sOutFileName, "w")

cap = cv2.VideoCapture("sample_video.mov")          # put test video here
means_ = []

while(cap.isOpened()):
    ret, frame = cap.read()
    if not ret:
        break
    (height, width, channels) = frame.shape
    cropFrame = frame[int(height/2-150):int(height/2+150), int(width/2-150):int(width/2+150), 0]  # 300x300
    mean = np.mean(cropFrame, dtype=np.float64)
    means_.append(mean)

cap.release()
cv2.destroyAllWindows()

filter_ = [0.0043, 0.0129, 0.0349, 0.0583, 0.0684, 0.0583, 0.0349, 0.0129, 0.0043]
meanFiltered = np.convolve(means_, filter_, 'same')
fftMeanFiltered = abs(np.fft.fft(meanFiltered))
fftMeanFiltered[0] = 0

frameCount = len(meanFiltered)
fourierMean = np.mean(fftMeanFiltered[:100])
fourierPos = []
fourierValues = []

for i in range(100):
    if fftMeanFiltered[i] > fourierMean:
        fourierPos.append(i)
        fourierValues.append(round(fftMeanFiltered[i], 5))

frequencies = []

for i in range(len(fourierPos)):
    frequencies.append(round((fourierPos[i]*30.0)/frameCount, 5))

bpm = []

for i in range(len(frequencies)):
    bpm.append(round(frequencies[i]*60, 5))

factors = {}
for i in range(len(bpm)):
    if frequencies[i] >= 1:
        factors[((fourierValues[i]*bpm[i])/frequencies[i])] = bpm[i]

max_ = max(factors.keys())
print('Pulse: ' + str(factors[max_]) + ' BPMs')               # display value
outFile.write(str('Pulse: ' + str(factors[max_]) + ' BPMs'))  # save value to a file
outFile.close()
