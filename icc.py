import requests
import json

def fetch_and_convert():
    url = "https://psplay.online/icctv/lol.php"
    output_file = "icc.m3u"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") == "success":
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n")
                
                for stream in data.get("live_streams", []):
                    title = stream.get("title", "Unknown Match")
                    manifest_url = stream.get("manifest_Url", "")
                    clearkey = stream.get("keys", "")
                    thumbnail = stream.get("match", {}).get("thumbnail", "")
                    
                    # Formatting for TiviMate/OTT Navigator ClearKey support
                    # Pattern: KIDs:KEYs
                    f.write(f'#EXTINF:-1 tvg-logo="{thumbnail}" group-title="𝐈𝐂𝐂",{title}\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={clearkey}\n')
                    f.write(f'{manifest_url}\n')
            
            print(f"Successfully generated {output_file}")
        else:
            print("Failed to fetch data: Status not success")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_convert()
