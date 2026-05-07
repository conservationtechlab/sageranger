from get_cam_location import cam_location

def main():
   """Tests get cam locations"""
   coordinates, id = cam_location("<cam name>", "<token>")
   print("Coordintes and ID:", coordinates, id)
      

if __name__ == "__main__":
    main()
