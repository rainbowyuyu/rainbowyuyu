
function copyToClipboard(platform) {
let textToCopy;

// 根据平台选择需要复制的号码
if (platform === 'wechat') {
  textToCopy = 'rainbow_465936509';  // 这里替换为你的微信号
} else if (platform === 'qq') {
  textToCopy = '465936509';  // 这里替换为你的QQ号
}

// 创建一个文本输入框来选择和复制文本
let tempInput = document.createElement('input');
document.body.appendChild(tempInput);
tempInput.value = textToCopy;
tempInput.select();  // 选择文本
document.execCommand('copy');  // 执行复制命令
document.body.removeChild(tempInput);  // 移除临时的输入框

// 提示用户已复制
alert('Copied ' + platform + ' number: ' + textToCopy);
}


document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form input values
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const subject = document.getElementById('subject').value;
    const message = document.getElementById('message').value;

    // Form validation
    if (!name || !email || !subject || !message) {
        showFeedback('Please fill in all fields.', 'error');
        return;
    }

    // Send data (for this example, we'll simulate a success response)
    setTimeout(() => {
        // Simulate successful form submission
        showFeedback('Your message has been sent successfully!', 'success');

        // Reset the form fields
        document.getElementById('contact-form').reset();
    }, 1000);
});

function showFeedback(message, type) {
    const feedbackElement = document.getElementById('form-feedback');
    feedbackElement.textContent = message;
    feedbackElement.className = type === 'error' ? 'error' : '';
}
