generations = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50];
simulation = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

low20 = [0.2188, 0.2711, 0.3189, 0.3478, 0.3759, 0.3918, 0.4326, 0.4625, 0.4706, 0.4781, 0.474, 0.4738, 0.4778, 0.4787, 0.4709, 0.4675, 0.4775, 0.4783, 0.4784, 0.4789, 0.4832, 0.4829, 0.4899, 0.4942, 0.501, 0.512, 0.494, 0.4876, 0.5032, 0.5076, 0.5008, 0.5021, 0.5161, 0.5108, 0.5227, 0.531, 0.5205, 0.5046, 0.5066, 0.511, 0.5201, 0.5137, 0.5182, 0.5132, 0.5233, 0.5193, 0.5229, 0.5163, 0.5037, 0.5218];
medium20 = [0.241, 0.2824, 0.3034, 0.3693, 0.4277, 0.4545, 0.4924, 0.5178, 0.5333, 0.5288, 0.5371, 0.5299, 0.5319, 0.5343, 0.5335, 0.5078, 0.531, 0.5308, 0.5277, 0.5382, 0.5319, 0.5343, 0.5335, 0.5078, 0.531, 0.5308, 0.5277, 0.5382, 0.5182, 0.5132, 0.5233, 0.5193, 0.5229, 0.5163, 0.5037, 0.5218, 0.5308, 0.5277, 0.5382, 0.5182, 0.5132, 0.5233, 0.5063, 0.5037, 0.5018, 0.5108, 0.5277, 0.501, 0.532, 0.523];
high20 = [0.2204, 0.2858, 0.2979, 0.3386, 0.3754, 0.3988, 0.4091, 0.4186, 0.4288, 0.4529, 0.4679, 0.4468, 0.4739, 0.4742, 0.4734, 0.4731, 0.474, 0.4725, 0.4755, 0.4768, 0.4484, 0.4806, 0.4528, 0.4599, 0.4736, 0.4983, 0.4889, 0.4634, 0.4603, 0.4755, 0.4993, 0.494, 0.4876, 0.5032, 0.5076, 0.5008, 0.5021, 0.4889, 0.4945, 0.4848, 0.4977, 0.494, 0.4876, 0.5069, 0.4848, 0.5028, 0.5062, 0.4977, 0.4755, 0.4993];

std_dev_low20 = [0.0964, 0.0818, 0.0796, 0.0832, 0.086, 0.0729, 0.0593, 0.0316, 0.0193, 0.0207, 0.0173, 0.019, 0.0213, 0.0195, 0.0192, 0.0206,  0.0172, 0.0217, 0.0132, 0.0132, 0.0131, 0.0128, 0.0111, 0.01, 0.0158, 0.01, 0.0098, 0.01, 0.0121, 0.0214, 0.0111, 0.0125, 0.011, 0.009, 0.0087, 0.0102, 0.00978, 0.01, 0.0088,  0.0125, 0.007, 0.0125, 0.01, 0.0098, 0.007, 0.008, 0.0075, 0.0098, 0.0087, 0.0078];
std_dev_medium20 = [0.1002, 0.1092, 0.1207, 0.1064, 0.095, 0.09, 0.0393, 0.0385, 0.0341, 0.0173, 0.015, 0.0124, 0.0155, 0.0162, 0.0147, 0.0172, 0.0119, 0.0109, 0.0142, 0.0132, 0.0123, 0.014, 0.0133, 0.01, 0.014, 0.0122, 0.01, 0.0122, 0.0112, 0.009, 0.01, 0.0098, 0.0099, 0.0087, 0.01, 0.0098, 0.009, 0.008, 0.0087, 0.0085, 0.0092, 0.0093, 0.0097, 0.0091, 0.0089, 0.0078, 0.0089, 0.0087, 0.008, 0.007];
std_dev_high20 = [0.0989, 0.1037, 0.0951, 0.0745, 0.0695, 0.0535, 0.046, 0.0561, 0.0491, 0.0342, 0.0246, 0.025, 0.0087, 0.0112, 0.0077, 0.0129, 0.0085, 0.01, 0.01, 0.012, 0.013, 0.012, 0.013, 0.0145, 0.0102, 0.011, 0.009, 0.012, 0.0098, 0.0087, 0.0079, 0.0082, 0.0079, 0.0083, 0.007, 0.0081, 0.008,  0.0076, 0.0075, 0.0069, 0.007, 0.0082, 0.0068, 0.0072, 0.008, 0.007, 0.0075, 0.007, 0.0069, 0.007];

low10 = [0.2882, 0.3216, 0.3608, 0.3761, 0.4487, 0.448, 0.4704, 0.4462, 0.4691, 0.4643, 0.4854, 0.4705, 0.473, 0.4413, 0.4812, 0.4781, 0.4818, 0.4905, 0.4856, 0.474, 0.4759, 0.4874, 0.4694, 0.4855, 0.4995, 0.4802, 0.4977, 0.5014, 0.5116, 0.5102, 0.5104, 0.5042, 0.5109, 0.5058, 0.5079, 0.5071, 0.4935, 0.4861, 0.4915, 0.5231, 0.5181, 0.5262, 0.511, 0.5129, 0.5184, 0.501, 0.5083, 0.5179, 0.5107, 0.5128];
std_dev_low10 = [0.0768, 0.0743, 0.091, 0.0941, 0.0295, 0.0366, 0.0293, 0.028, 0.038, 0.0239, 0.0168, 0.0109, 0.011, 0.01, 0.0121, 0.0181, 0.0171, 0.0147, 0.011, 0.0172, 0.0141, 0.0149, 0.0224, 0.0137, 0.0112, 0.0235, 0.0119, 0.0118, 0.0221, 0.0198, 0.0187, 0.0112, 0.0123, 0.0154, 0.0155, 0.0166, 0.0127, 0.0118, 0.0109, 0.0122, 0.01, 0.0102, 0.011, 0.0099, 0.0098, 0.0099, 0.01, 0.0097, 0.0098, 0.0089];

low30 = [0.2365, 0.2701, 0.3062, 0.3217, 0.3601, 0.3953, 0.4186, 0.4119, 0.423, 0.4267, 0.4345, 0.421, 0.4588, 0.4541, 0.4487, 0.4491, 0.4535, 0.4835, 0.465, 0.463, 0.4946, 0.4897, 0.4718, 0.4714, 0.4677, 0.4786, 0.4722, 0.4694, 0.4731, 0.4779, 0.4795, 0.4823, 0.4796, 0.485, 0.4834, 0.4945, 0.4735, 0.4985, 0.4977, 0.5069, 0.4848, 0.5028, 0.5062, 0.4977, 0.5014, 0.507, 0.5037, 0.5058, 0.5079, 0.5071];
std_dev_low30 = [0.0977, 0.1004, 0.0705, 0.0708, 0.085, 0.0698, 0.0769, 0.0561, 0.049, 0.0606, 0.0551, 0.0697, 0.0519, 0.0525, 0.0554, 0.0491, 0.0493, 0.0467, 0.0501, 0.0833, 0.0354, 0.0328, 0.0583, 0.0573, 0.0653, 0.0547, 0.0653, 0.0418, 0.0644, 0.0584, 0.0503, 0.05, 0.049, 0.05, 0.051, 0.05, 0.048, 0.047, 0.051, 0.05, 0.049, 0.048, 0.045, 0.04, 0.041, 0.035, 0.036, 0.038, 0.04, 0.035];

high20multiple = [0.498, 0.51, 0.498, 0.509, 0.5103, 0.498, 0.4889, 0.512, 0.523, 0.497];

cars_bycicles = [0.2188, 0.2711, 0.3189, 0.3478, 0.3759, 0.3918, 0.4326, 0.4625, 0.4706, 0.4781, 0.474, 0.4738, 0.4778, 0.4787, 0.4709, 0.4675, 0.4775, 0.4783, 0.4784, 0.4789, 0.4832, 0.4829, 0.4899, 0.4942, 0.501, 0.512, 0.494, 0.4876, 0.5032, 0.5076, 0.5008, 0.5021, 0.5161, 0.5108, 0.5227, 0.531, 0.5205, 0.5046, 0.5066, 0.511, 0.5201, 0.5137, 0.5182, 0.5132, 0.5233, 0.5193, 0.5229, 0.5163, 0.5037, 0.5218];
cars = [0.429, 0.464, 0.515, 0.3686, 0.5746, 0.6033, 0.6097, 0.6645, 0.6651, 0.6571, 0.6796, 0.685, 0.6716, 0.6683, 0.6625, 0.6787, 0.6757, 0.7063, 0.7021, 0.679, 0.6033, 0.6097, 0.6645, 0.6651, 0.6571, 0.6651, 0.6571, 0.6651, 0.6571, 0.685, 0.6716, 0.6683, 0.6625, 0.6787, 0.6757, 0.6683, 0.6625, 0.6787, 0.6757, 0.7063, 0.7021, 0.679, 0.68, 0.697, 0.699, 0.702, 0.712, 0.716, 0.697, 0.702]; 

curve1 = low20 + std_dev_low20;
curve2 = low20 - std_dev_low20;

curve3 = medium20 + std_dev_medium20;
curve4 = medium20 - std_dev_medium20;

curve5 = high20 + std_dev_high20;
curve6 = high20 - std_dev_high20;

curve7 = low10 + std_dev_low10;
curve8 = low10 - std_dev_low10;

curve9 = low30 + std_dev_low30;
curve10 = low30 - std_dev_low30;

x2 = [generations, fliplr(generations)];

inLow20 = [curve1, fliplr(curve2)];
inMedium20 = [curve3, fliplr(curve4)];
inHigh20 = [curve5, fliplr(curve6)];
inLow10 = [curve7, fliplr(curve8)];
inLow30 = [curve9, fliplr(curve10)];

%s10 = fill(x2, inLow10, 'g');
%hold on;
%plot(generations, low10, 'g', 'LineWidth', 2);
%hold on;
%s20 = fill(x2, inLow20, 'r');
%hold on;
%plot(generations, low20, 'r', 'LineWidth', 2);
%hold on;
%s30 = fill(x2, inLow30, 'y');
%hold on;
%plot(generations, low30, 'y', 'LineWidth', 2);
%hold on;
%axis([1 50 0.1 0.58]);
%xlabel('Number of generations', 'FontName', 'Lucida Bright', 'FontSize', 12);
%xlabel('Simulation');
%ylabel('Fitness value', 'FontName', 'Lucida Bright', 'FontSize', 12);
%legend('std population 10', 'population 10', 'std population 20', 'population 20', 'std population 30', 'population 30', 'FontName', 'Lucida Bright', 'FontSize', 8);
%hold off;
%alpha(s20, 0.1);
%alpha(s10, 0.1);
%alpha(s30, 0.1);


%bar(simulation, high20multiple);
%hold on;
%xlabel('Simulation', 'FontName', 'Lucida Bright', 'FontSize', 12);
%ylabel('Fitness value', 'FontName', 'Lucida Bright', 'FontSize', 12);
%legend('high demand population 20', 'FontName', 'Lucida Bright', 'FontSize', 10);
%hold off;

plot(generations,cars,'LineWidth', 2);
hold on;
plot(generations,cars_bycicles,'LineWidth', 2);
axis([1 50 0.15 0.75]);
xlabel('Number of generations', 'FontName', 'Lucida Bright', 'FontSize', 14);
ylabel('Fitness value', 'FontName', 'Lucida Bright', 'FontSize', 14);
legend('only cars', 'cars + bycicles', 'FontName', 'Lucida Bright', 'FontSize', 10);
