var customBarColors = {
  success: '#28a745',
  error: '#dc3545',
  ignored: '#7a7a7a',
  progress: '#007bff',
}

function customProgress(progressBarElement, progressBarMessageElement, progress) {
  if (progress.current == 0) {
    if (progress.pending === true) {
      progressBarMessageElement.textContent = 'Waiting for task to start...';
    } else {
      progressBarMessageElement.textContent = 'Task started...';
    }
  } else {
    progressBarMessageElement.textContent = progress.description;
  }
  progressBarElement.style.width = String(progress.percent) + "%";
  progressBarElement.style.background = this.barColors.progress;
}

function customSuccess(progressBarElement, progressBarMessageElement) {
  progressBarElement.style.background = this.barColors.success;
  progressBarMessageElement.innerHTML = 'Analysis Completed!';
}

function customResult(progressBarElement, progressBarMessageElement){
  progressBarElement.style.background = this.barColors.success;
  progressBarMessageElement.innerHTML = 'Analysis Completed!';
}

function customError(progressBarElement, progressBarMessageElement) {
  progressBarElement.style.background = this.barColors.error;
  progressBarMessageElement.innerHTML = 'Something Went Wrong!';
}
