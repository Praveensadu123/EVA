function validatelogin() {
    var username = document.getElementsByName("username")[0].value;
    var password = document.getElementsByName("password")[0].value;

    // Validate username and password constraints
    if (username.length < 6) 
    {
        alert("Username must be at least 6 characters.");
        return false;
    }
    else if (password.length < 8) 
    {
        alert("password must be at least 8 characters.");
        return false;
    }
    
    else if (password.length > 8) 
    {
        if (!(/\d/.test(password))) {
            alert("password must contain digits");
            return false;
        } 
        else if (!(/[A-Z]/.test(password))) {
            alert("password must contain capital letters");
            return false;
        } 
        else if (!(/[!@#$%^&*(),.?":{}|<>]/.test(password))) {
            alert("password must contain special characters Ex: @, #, $ etc...");
            return false;
        }
    }
    

    // Additional constraints can be added if needed

    // If validation passes, you can submit the form
    // Example: document.getElementById("loginForm").submit();

    return true; // Form submission allowed
}