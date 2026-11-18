import requests

from app.config.settings import COMPREFACE_CONFIG


def recognize_faces(image_bytes):
    """
    Detect and recognize faces in the given image bytes using CompreFace.
    Returns a list of recognized subjects and their bounding boxes.
    """
    host = COMPREFACE_CONFIG.get("host")
    api_key = COMPREFACE_CONFIG.get("api_key")
    
    if not host or not api_key:
        return []
        
    try:
        url = f"{host}/api/v1/recognition/recognize"
        headers = {
            "x-api-key": api_key
        }
        
        # We need to send the image as multipart/form-data
        files = {
            'file': ('image.jpg', image_bytes, 'image/jpeg')
        }
        
        response = requests.post(url, headers=headers, files=files, timeout=10)
        
        if response.status_code != 200:
            print(f"CompreFace Error: {response.status_code} - {response.text}")
            return []
            
        data = response.json()
        results = data.get("result", [])
        
        faces = []
        for r in results:
            # CompreFace returns an array of subjects, usually we take the most confident one
            subjects = r.get("subjects", [])
            subject_name = None
            confidence = 0.0
            
            if subjects:
                # Top match
                subject_name = subjects[0].get("subject")
                confidence = subjects[0].get("similarity", 0.0)
                
            box = r.get("box", {})
            
            faces.append({
                "subject": subject_name,
                "confidence": confidence,
                "box": box
            })
            
        return faces
    except Exception as e:
        print(f"CompreFace face recognition failed: {e}")
        return []
