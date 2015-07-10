
% Constants
offset = 6;
x = offset + linspace(-9, 9, 1000);

mu = offset + [0 4]; 
sigma = [1 2];
color = [79 129 189; 192 80 77] / 256;

clf;

% Loop over plot
for pl = 1:2
  % Create subplot
  if(pl == 1)
    subplot(3, 1, [1 2]); cla; hold on;
  else
    subplot(3, 1, [3]); cla; hold on;
  end

  % Set limits
  xlim(offset + [-9 9]);

  % Draw vertical line
  h = line(offset + [0 0], [0 1], 'HandleVisibility', 'off');  
  set(h, 'LineStyle', '--');
  set(h, 'Color', 'k');

  % Draw horizontal line in first plot
  if(pl == 1)
    h = line(offset + [-10 10], [0.5 0.5], 'HandleVisibility', 'off');
    set(h, 'LineStyle', '--');
    set(h, 'Color', 'k');
  end

  
  for i = 1:2  
    % CDF for first plot, PDF for second
    if(pl == 1)
      p = normcdf(x, mu(i), sigma(i));
    else
      p = normpdf(x, mu(i), sigma(i));
    end

    % Create plot
    h = plot(x, p);
    set(h, 'LineWidth', 2);
    set(h, 'Color', color(i, :));  
  
    % Create bars at SD
    S = mu(i) + ([-1 1] * sigma(i));  
    c = color(i, :) * 0.5 + 0.5;
    
    if(pl == 1)
      height = 0.5;
      height2 = 0.5;
    else
      height = normpdf(mu(i) - sigma(i), mu(i), sigma(i));
      height2 = normpdf(mu(i), mu(i), sigma(i));
    end
  
    h = plot(S, height * [1 1], 'HandleVisibility', 'off');
    set(h, 'LineWidth', 2);
    set(h, 'Color', c);
    
    h = plot(mu(i), height2, 'o', 'HandleVisibility', 'off');
    set(h, 'MarkerFaceColor', c);
    set(h, 'MarkerEdgeColor', c);
  
    for j = 1:2
      sign = (j - 1.5) * 2;
      h = plot(S(j) - sign * [0 0.5], height + [0 0.03], 'HandleVisibility', 'off');
      set(h, 'LineWidth', 2);
      set(h, 'Color', c);
      
      h = plot(S(j) - sign * [0 0.5], height - [0 0.03], 'HandleVisibility', 'off');
      set(h, 'LineWidth', 2);
      set(h, 'Color', c);
      
      %h = plot(S(j) + [0 0], [0 1], 'HandleVisibility', 'off');
      %set(h, 'Color', c);
      %set(h, 'LineStyle', '--');
    end  
  end

  % Legend and y-label for CDF plot
  if(pl == 1)
    h = legend({'Veridical', 'Biassed'});
    set(h, 'Location', 'NorthWest');

    ylabel(...
      'P(Response = 2nd longer)');
    
    set(gca, 'YTick', [0 0.5 1]);
    set(gca, 'XTick', []);    
  end

  % Ticks and labels for PDF
  if(pl == 2)
    ylim([0 0.45]);
    set(gca, 'XTick', -9:3:20);
    set(gca, 'YTick', []);
  
    xlabel(...
      'Probe distance (cm)', ...
      'FontSize', 10);
    ylabel('P');
  end

end
