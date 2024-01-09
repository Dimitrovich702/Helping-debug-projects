  <script>
     const executionTimeElement = document.getElementById('execution-time');
let startTime, endTime;
function startTimer() {
  startTime = performance.now();
}
function stopTimer() {
  endTime = performance.now();
  const executionTime = endTime - startTime;
  executionTimeElement.textContent = `Execution Time: ${executionTime}ms`;
}
startTimer();
// stuff that you would like to calculate 
stopTimer();

</script>
