"""
Quick Actions Module for IT Helpdesk Chatbot

This module contains all the Quick Action functions that simulate
various IT support operations. These functions are called from the
main chatbot UI to provide instant responses for common IT tasks.

Author: IT Helpdesk Chatbot System
Date: August 16, 2025
"""

def reset_password():
    """Simulates password reset process"""
    return """🔐 Password Reset Process Initiated

✅ Function called: reset_password()

Steps completed:
1. ✅ User identity verified
2. ✅ Temporary password generated: TempPass123!
3. ✅ Password reset email sent to user's registered email
4. ✅ User account flagged for mandatory password change on next login

⚠️ Please remind the user to:
- Check their email (including spam folder)
- Use the temporary password for the next login
- Create a strong new password following company policy
- Contact IT if they don't receive the reset email within 15 minutes"""

def request_admin_permission():
    """Simulates admin permission request process"""
    return """🔑 Admin Permission Request Submitted

✅ Function called: request_admin_permission()

Request details:
1. ✅ Permission request ticket created: #ADM-2024-0156
2. ✅ Request forwarded to IT Security team
3. ✅ User's manager notified for approval
4. ✅ Estimated approval time: 2-4 business hours

📋 Next steps:
- User will receive email confirmation within 5 minutes
- Manager approval required before IT can process
- Temporary admin access may be granted for urgent tasks
- User will be notified once permissions are activated"""

def unblock_account():
    """Simulates account unblock process"""
    return """🔓 Account Unblock Process Completed

✅ Function called: unblock_account()

Actions taken:
1. ✅ Account status verified - was locked due to multiple failed login attempts
2. ✅ Security check completed - no suspicious activity detected
3. ✅ Account successfully unlocked
4. ✅ Failed login counter reset

🔒 Security recommendations:
- Use strong, unique passwords
- Enable two-factor authentication if available
- Avoid password sharing
- Report any suspicious account activity immediately
- Consider using company password manager"""

def submit_ticket():
    """Simulates IT ticket submission"""
    return """🎫 IT Support Ticket Created

✅ Function called: submit_ticket()

Ticket Information:
- Ticket ID: #ITK-2024-0789
- Priority: Standard
- Category: General IT Support
- Status: Open
- Assigned to: IT Support Queue

📞 Contact Information:
- Email updates will be sent automatically
- For urgent issues, call: (555) 123-4567
- Estimated response time: 4-6 business hours
- You can track ticket status using the ticket ID above"""

def request_wifi_access():
    """Simulates WiFi access request"""
    return """📶 WiFi Access Request Processed

✅ Function called: request_wifi_access()

Network Configuration:
1. ✅ Guest network access enabled
2. ✅ Temporary credentials generated
3. ✅ Access valid for 24 hours
4. ✅ Bandwidth: Standard business profile

🌐 Connection Details:
- Network Name: CompanyGuest
- Password: Guest2024Temp
- Valid until: Tomorrow at this time
- For extended access, please contact your department admin
- Corporate network access requires different authorization process"""

# Function registry for easy access and extensibility
QUICK_ACTIONS = {
    'reset_password': reset_password,
    'request_admin_permission': request_admin_permission,
    'unblock_account': unblock_account,
    'submit_ticket': submit_ticket,
    'request_wifi_access': request_wifi_access
}

def get_quick_action(action_name):
    """
    Get a quick action function by name
    
    Args:
        action_name (str): Name of the action function
        
    Returns:
        function: The corresponding action function, or None if not found
    """
    return QUICK_ACTIONS.get(action_name)

def list_available_actions():
    """
    Get a list of all available quick actions
    
    Returns:
        list: List of available action names
    """
    return list(QUICK_ACTIONS.keys())
