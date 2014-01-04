partA = 1:16;
partB = 16:34;
partC = 34:55;
partD = 55:70;

partAy = exp(0.3 * partA);

partBy = 2 * (partB - partA(end)) + partAy(end);

partCy = -1 * (partC - partB(end)) + partBy(end);

partDy = -exp(0.325 * (partD - partC(end))) + partCy(end);

close all;
figure;

hold on;
plot(partA, partAy);
plot(partB, partBy, 'r');
plot(partC, partCy, 'c');
plot(partD, partDy, 'm');
set(gca, 'ytick', []);
xlabel('Total steps');
ylabel('Branching factor');
title('Branching factor throughout a Blokus game');
legend('Part A', 'Part B', 'Part C', 'Part D');