document.addEventListener('DOMContentLoaded', function() {
    // Find all code blocks created by CKEditor's CodeSnippet plugin
    const codeBlocks = document.querySelectorAll('pre code[class*="language-"]');
    
    codeBlocks.forEach((codeBlock, index) => {
        const pre = codeBlock.parentElement;
        const language = getLanguageFromClass(codeBlock.className);
        
        // Only add run button for supported languages
        if (['python', 'javascript', 'js', 'html'].includes(language)) {
            addRunButton(pre, codeBlock, language, index);
        }
    });
});

function getLanguageFromClass(className) {
    const match = className.match(/language-(\w+)/);
    if (!match) return 'text';
    
    const lang = match[1].toLowerCase();
    // Map common variations
    if (lang === 'js') return 'javascript';
    if (lang === 'py') return 'python';
    return lang;
}

function addRunButton(pre, codeBlock, language, index) {
    // Create wrapper for code block with controls
    const wrapper = document.createElement('div');
    wrapper.className = 'code-runner-wrapper';
    wrapper.style.cssText = `
        position: relative;
        margin: 20px 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    `;
    
    // Create header with language badge and run button
    const header = document.createElement('div');
    header.className = 'code-runner-header';
    header.style.cssText = `
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 10px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    `;
    
    const languageBadge = document.createElement('span');
    languageBadge.textContent = language.toUpperCase();
    languageBadge.style.cssText = `
        color: white;
        font-weight: bold;
        font-size: 12px;
        font-family: monospace;
    `;
    
    const runButton = document.createElement('button');
    runButton.innerHTML = '▶ Run Code';
    runButton.className = 'run-code-btn';
    runButton.style.cssText = `
        background: white;
        color: #667eea;
        border: none;
        padding: 8px 16px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        font-size: 14px;
        transition: all 0.3s;
    `;
    runButton.onmouseover = () => runButton.style.transform = 'scale(1.05)';
    runButton.onmouseout = () => runButton.style.transform = 'scale(1)';
    
    header.appendChild(languageBadge);
    header.appendChild(runButton);
    
    // Create output container
    const outputDiv = document.createElement('div');
    outputDiv.className = 'code-output';
    outputDiv.id = `output-${index}`;
    outputDiv.style.cssText = `
        background: #1e1e1e;
        color: #4caf50;
        padding: 15px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        white-space: pre-wrap;
        max-height: 300px;
        overflow-y: auto;
        display: none;
        border-top: 2px solid #667eea;
    `;
    outputDiv.textContent = 'Click "Run Code" to see output...';
    
    // Wrap everything
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(header);
    wrapper.appendChild(pre);
    wrapper.appendChild(outputDiv);
    
    // Add click handler
    runButton.addEventListener('click', () => {
        runCode(codeBlock.textContent, language, outputDiv, runButton);
    });
}

async function runCode(code, language, outputDiv, button) {
    outputDiv.style.display = 'block';
    outputDiv.textContent = 'Running...';
    button.disabled = true;
    button.innerHTML = '⏳ Running...';
    
    try {
        if (language === 'python') {
            await runPython(code, outputDiv);
        } else if (language === 'javascript') {
            runJavaScript(code, outputDiv);
        } else if (language === 'html') {
            runHTML(code, outputDiv);
        }
    } catch (error) {
        outputDiv.style.color = '#f44336';
        outputDiv.textContent = `Error: ${error.message}`;
    } finally {
        button.disabled = false;
        button.innerHTML = '▶ Run Code';
    }
}

async function runPython(code, outputDiv) {
    try {
        const response = await fetch('https://emkc.org/api/v2/piston/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                language: 'python',
                version: '3.10.0',
                files: [{ content: code }]
            })
        });
        
        const result = await response.json();
        outputDiv.style.color = '#4caf50';
        outputDiv.textContent = result.run.output || result.run.stderr || 'No output';
    } catch (error) {
        outputDiv.style.color = '#f44336';
        outputDiv.textContent = `Error: ${error.message}`;
    }
}

function runJavaScript(code, outputDiv) {
    const logs = [];
    const originalLog = console.log;
    const originalError = console.error;
    
    console.log = (...args) => {
        logs.push(args.map(arg => 
            typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
        ).join(' '));
    };
    
    console.error = (...args) => {
        logs.push('ERROR: ' + args.join(' '));
    };
    
    try {
        eval(code);
        outputDiv.style.color = '#4caf50';
        outputDiv.textContent = logs.length > 0 ? logs.join('\n') : 'Code executed successfully (no output)';
    } catch (error) {
        outputDiv.style.color = '#f44336';
        outputDiv.textContent = `Error: ${error.message}`;
    } finally {
        console.log = originalLog;
        console.error = originalError;
    }
}

function runHTML(code, outputDiv) {
    outputDiv.style.color = '#4caf50';
    outputDiv.style.background = 'white';
    outputDiv.style.padding = '0';
    outputDiv.style.maxHeight = '500px';
    
    const iframe = document.createElement('iframe');
    iframe.style.cssText = `
        width: 100%;
        height: 400px;
        border: none;
    `;
    
    outputDiv.innerHTML = '';
    outputDiv.appendChild(iframe);
    
    const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
    iframeDoc.open();
    iframeDoc.write(code);
    iframeDoc.close();
}