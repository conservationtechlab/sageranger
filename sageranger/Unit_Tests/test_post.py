from post_event_er import post_event

def main():
   """Tests creating an event"""
   
   event_id = post_event("<label>","<cam name>", "<token>")
   print("Event_ID:", event_id)
    

if __name__ == "__main__":
    main()
