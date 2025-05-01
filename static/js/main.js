// Document password verification
async function verifyPassword(docId) {
    const password = prompt('Please enter the document password:');
    if (!password) return;

    try {
        const response = await fetch('/verify-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });
        const data = await response.json();

        if (data.success) {
            window.location.href = `/document/${docId}`;
        } else {
            alert('Incorrect password');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while verifying the password');
    }
}

// Document upload handling
async function uploadDocument(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    try {
        const response = await fetch('/admin/upload', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (data.success) {
            alert('Document uploaded successfully');
            window.location.reload();
        } else {
            alert(data.error || 'Failed to upload document');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while uploading the document');
    }
}