from financeapp.models import Members
from math import floor

def usd(value):
    """Format value as USD."""

    if value < 0:
        return f"${floor(-(value)):,.2f}"

    return f"${floor(value):,.2f}"


def member_spending(current_user, detailed):
    members = Members.query.filter_by(user_id = current_user).all()

    members_data = {}

    if detailed:
        
        for member in members:

            members_data[member.name] = {}
            members_data[member.name]['spent'] = 0
            members_data[member.name]['income'] = 0
            members_data[member.name]['recieved'] = 0
            

            for item in member.trans_members:

                member_count = len(item.member_transactions)

                if item.paid_by == member.id:

                    if item.transaction_type == "Inc":  
                        members_data[member.name]['income'] += item.amount

                    if item.transaction_type == "Ex":
                        members_data[member.name]['spent'] += (item.amount / member_count)
                        members_data[member.name]['income'] += -(item.amount)

                else:
                    if item.transaction_type == "Ex":
                        members_data[member.name]['spent'] += (item.amount / member_count)
                    else:    
                        members_data[member.name]['recieved'] += (item.amount / member_count)
                        members_data[members[(item.paid_by - 1)].name]['income'] += (item.amount)


        for member in members_data.keys():
            members_data[member]['balance'] = floor(members_data[member]['spent'] + (members_data[member]['income'] - members_data[member]['recieved']))
           
        return members_data
            

    for member in members:
        members_data[member.name] = {}
        member_spent = 0
        member_income = 0
        member_recieved = 0

        for item in member.trans_members:
            member_count = len(item.member_transactions)

            if item.paid_by == member.id:

                if item.transaction_type == "Inc":  
                    member_income += item.amount

                if item.transaction_type == "Ex":
                    member_spent += (item.amount / member_count)
                    member_income += -(item.amount)

            else:
                if item.transaction_type == "Ex":
                    member_spent += (item.amount / member_count)
                else:    
                    member_recieved += (item.amount / member_count)
                    members_data[members[(item.paid_by - 1)].name]['balance'] += (item.amount)
                    
            
        members_data[member.name]['balance'] = floor(member_spent + (member_income - member_recieved))
    
    return members_data