console.log('Begin...');

let interval = setInterval(function () {
    if (document.readyState === 'complete') {
        clearInterval(interval);
        myMain();
    }
}, 1000);

function myMain() {
    document.querySelector('div#todoStack').addEventListener('scroll', function () {
        const content = this;
        if (content.scrollTop + content.clientHeight >= content.scrollHeight - 1) {
            content.classList.add('bounce');
            setTimeout(() => {
                content.classList.remove('bounce');
            }, 500);
        } else {
            if (content.scrollTop <= 0) {
                content.classList.add('debounce');
                setTimeout(() => {
                    content.classList.remove('debounce');
                }, 500);
            }
        }
    });
    // Select the nodes that will be observed for changes
    let element = document.querySelector('div#scrollbarDiv');
    let input = document.querySelector('input#messageInput');
    element.scrollTop = element.scrollHeight;
    input.focus();

    // Options for the observer (which mutations to observe)
    let callback = function (mutationsList, observer) {
        element.scrollTop = element.scrollHeight;
    };
    let callback_input = function (mutationsList, observer) {
        for (const mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'disabled') {
                let isDisabled = input.getAttribute('disabled') !== null;
                if (!isDisabled) {
                    input.focus();
                }
            }
        }
    };

    // Create an observer instance linked to the callback function
    let observer = new MutationObserver(callback);
    observer.observe(element, {childList: true, subtree: true});
    let observer_input = new MutationObserver(callback_input);
    observer_input.observe(input, {attributes: true, childList: false, subtree: false});
}