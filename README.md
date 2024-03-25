# Using-CNNs-in-Bushfire-Research

## Introduction
In the 21st century, Australia experienced two devastating bushfires that impacted the nation’s history. Except for the environmental and economical impacts, these catastrophic bushfires also caused severe climate change and biodiversity issues. To mitigate the influences of potential future large-scale bushfires, monitoring and
forecasting models are of vital importance. Satellite images, which encompass multiple spectral bands, collectively capture various features on earth surface. Such characteristics make them ideal inputs for monitoring bushfires. Recently, Convolutional Neural Networks (CNNs) have shown remarkable efficacy in the field of image recognition. Therefore, the combination
of satellite imagery and CNNs has become an effective solution to solve bushfire detection problems. In this research, we aim to exploit a variety of CNNs to productively identify areas that are at the highest risk of fires, specifically by analysing the levels of hydration and carbon content.

## Supervisors
- Richard Sinnott (rsinnott@unimelb.edu.au)
- Luca Morandini (luca.morandini@unimelb.edu.au)

## Tech Stack
- Satellite Imagery
- Convolutional Neural Network
- Data Augmentation
- High Performance Computing (Spartan)

## Data
### Area of Interest
We mainly focused on the ”Black Summer” bushfires and selected the most bushfire-affected areas in the south-eastern coast of Australia,. In addition, every red dot in the picture represents a individual bushfire, and sizes can be regarded as the scales of bushfires.
<img width="304" alt="area-of-interest" src="https://github.com/jo-muuuuuu/Bushfire-Research-Using-CNNs/assets/142861960/392dab5c-e80d-41f7-9d2e-f320a721efad">

### Dataset
Based on the areas selected, we prepared a dataset covered the time range from 1st Jul 2019 to 1st Jul 2020, which matches the time range of the ”Black Summer”. However, this dataset does not include images of the whole year, since the revisit time of Sentinel 2 - L2A satellite is 5 days.

## Convolutional Nueral Network (CNN)
Similar to traditional Artificial Neural Networks (ANNs), CNNs are also structured with multiple layers stacked sequentially. These layers (also called hidden layers) incorporate neurons, which are able to self-optimize through learning, to carry out computational tasks. However, CNNs have several outstanding advantages: 
1. CNNs typically reduce the size of the input as the depth increases, which means the number of parameters is reduced constantly. 
2. Weights are shared across nodes and connections, which can further decrease the number of parameters. 
3. Due to the nature of convolutinal and pooling layers, CNNs can extract abstract features more accurately as the input propagates toward deeper layers. As a result, CNNs are capable of addressing computational difficult problems with relatively simple structures, making it an ideal solution to deal with excessively large inputs.

## CNNs used
- `LeNet-5`
- `U-Net`
- `EfficientNet` - B5 & B6
- `ResNet` - 50 Layers & 101 Layers
  
## Results
Serveral CNNs produced the same suboptimal output although they vary in architectures and complexities. This phenomenon indicates that the main reason is due to the limited dataset volume. 

The top-performing models in the table consistently achieve metrics around 93% for both accuracy and precision, and nearly 100% recall. Those values proved that our models can almost identify all burned images correctly, and making true predictions at the same time.

<img width="525" alt="results-table" src="https://github.com/jo-muuuuuu/Bushfire-Research-Using-CNNs/assets/142861960/e3c9aa21-e2a0-47b5-a0c5-bd78f97c1028">
