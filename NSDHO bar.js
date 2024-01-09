//NSDHSO — Today at 9:13 AM
//Hi folks, I have a question, has cnv worked with d3.js before? I don't like its very imperative format,
//you can't really change anything through the base code. just for a gradient bar 
//I wrote about 200 lines of code, do you have an idea how I could extrapolate this idea and go towards functional programming??
///
const width = 600;
      const height = 420;
      const margin = { top: 0, bottom: 30, left: 30, right: 20 };

      const svg = createNewSvg('#gradient', '100%', '100%', d3);

      const gradientAndXAxis = createNewGroup(svg);
      gradientAndXAxis.attr('transform', `translate(0, 30)`); // Ajustare pentru poziționare]
      const gradient = gradientAndXAxis
        .append('defs')
        .append('linearGradient')
        .attr('id', 'bar-gradient')
        .attr('x1', '0%')
        .attr('y1', '0%')
        .attr('x2', '100%')
        .attr('y2', '0%');
      this.gradientSettings.forEach((setting: Any) => {
        gradient
          .append('stop')
          .attr('offset', setting.offset)
          .attr('stop-color', setting.stopColor);
      });
      gradientAndXAxis
        .append('rect')
        .attr('x', 0)
        .attr('y', 0)
        .attr('width', '100%')
        .attr('height', 10)
        .transition() // Apply transition effect
        .duration(500)
        .style('fill', 'url(#bar-gradient)');

      const xScale = d3
        .scaleLinear()
        .domain(this.range) // Assuming the domain ranges from 1 to 5
        .range([margin.left, width - margin.right]); // Adjust according to your chart's margins

      // Create an x-axis using the xScale
      const xAxis = d3
        .axisBottom(xScale)
        .ticks(this.range[this.range.length - 1]) // Set the number of ticks as needed
        .tickFormat(d3.format('d')); // Format the tick labels as integers

      // Append the x-axis to your SVG
      function updateXAxis(range: Any) {
        const svgWidth = parseFloat(svg.style('width').replace('px', '')); // Lățimea SVG-ului

        // Actualizarea scalei pentru axa x
        const xScale = d3
          .scaleLinear()
          .domain(range) // Intervalul sau domeniul barelor tale
          .range([0, svgWidth - margin.left]); // Ajustarea la dimensiunea SVG-ului

        // Șterge bara de pe axa x existentă (dacă există deja)
        gradientAndXAxis.select('.x-axis').remove();

        // Adăugarea barelor pentru axa x actualizată
        const xAxis = d3.axisBottom(xScale).ticks(range[range.length - 1]); // Numărul de bare pe axa x

        const xAxiss = createNewGroup(gradientAndXAxis)
          .attr('class', 'x-axis')
          .attr('transform', `translate(10, 10)`) // Ajustare pentru poziționare]
          .transition() // Apply transition effect
          .duration(500)
          .call(xAxis);

        // Stilizare bare axă x
        xAxiss.selectAll('.tick line').remove(); // Ascunde liniile de marcaj

        xAxiss
          .selectAll('.tick text')
          .style('fill', 'white')
          .style('font-size', '12px'); // Stilizare text

        gradientAndXAxis.select('.marker-group').remove();
        gradientAndXAxis.select('.between-group').remove();

        // Create a new group for the marker and associated elements
        const markerGroup = gradientAndXAxis
          .append('g')
          .attr('class', 'marker-group')
          .attr('transform', `translate(10, 0)`); // Ajustare pentru poziționare

        // Add the bar on the x-axis
        markerGroup
          .append('rect')
          .attr('x', xScale(3))
          .attr('y', 0)
          .attr('width', 3)
          .attr('height', 10)
          .transition() // Apply transition effect
          .duration(500)
          .style('fill', 'white');

        // Add the marker line
        markerGroup
          .append('line')
          .attr('x1', xScale(3))
          .attr('y1', 0)
          .attr('x2', xScale(3))
          .attr('y2', 10)
          .style('stroke', 'white')
          .transition() // Apply transition effect
          .duration(500)
          .attr('marker-end', 'url(#arrowhead)');
        // Apelarea funcției pentru a inițializa barele pe axa x
        // Add a background rectangle behind the text labe

        markerGroup
          .append('rect')
          .attr('x', xScale(3) - 40) // Adjusted x-position to center the text
          .attr('y', -20) // Adjusted y-position to move the background rectangle
          .attr('width', 80) // Adjusted width for the background rectangle
          .attr('height', 15) // Adjusted height for the background rectangle
          .style('fill', 'gray') // Background color
          .style('rx', '5px') // Rounded corner
          .style('ry', '5px'); // Rounded corner

        // Add the text label above the marker
        markerGroup
          .append('text')
          .attr('x', xScale(3))
          .attr('y', -10) // Adjusted position to move the text closer to the marker
          .text('You are here')
          .attr('text-anchor', 'middle')
          .attr('fill', 'white')
          .attr('font-size', '10px');

        const betweenFourAndFiveGroup = createNewGroup(gradientAndXAxis)
          .attr('class', 'between-group')
          .attr('transform', `translate(10, 0)`);
        const xPos4 = xScale(1);
        const xPos5 = xScale(5);
        betweenFourAndFiveGroup
          .append('rect')
          .attr('x', xScale(4.5) - 60) // Adjusted x-position to center the text
          .attr('y', -20) // Adjusted y-position to move the background rectangle
          .attr('width', 120) // Adjusted width for the background rectangle
          .attr('height', 15) // Adjusted height for the background rectangle
          .style('fill', 'gray') // Background color
          .style('rx', '5px') // Rounded corner
          .style('ry', '5px'); // Rounded corner
        betweenFourAndFiveGroup
          .append('text')
          .attr('x', xScale(4.5)) // Adjusted x-position for the text label
          .attr('y', -10) // Adjusted y-position for the text label
          .text('You should be here')
          .attr('text-anchor', 'middle')
          .attr('fill', 'white')
          .attr('font-size', '10px');
        const markerSecond = createNewGroup(betweenFourAndFiveGroup);
        // Add a rectangle for visual reference
        markerSecond
          .append('rect')
          .attr('x', xScale(4)) // Adjusted x-position for the rectangle
          .attr('y', -10) // Adjusted y-position for the rectangle
          .attr('width', 2) // Adjusted width for the rectangle
          .attr('height', 20) // Adjusted height for the rectangle
          .style('fill', 'lightblue'); // Background color for the rectangle

        markerSecond
          .append('rect')
          .attr('x', xScale(5)) // Adjusted x-position for the rectangle
          .attr('y', -10) // Adjusted y-position for the rectangle
          .attr('width', 2) // Adjusted width for the rectangle
          .attr('height', 20) // Adjusted height for the rectangle
          .style('fill', 'lightblue'); // Background color for the rectangle
        // Add the text label in the middle of the interval
      }
