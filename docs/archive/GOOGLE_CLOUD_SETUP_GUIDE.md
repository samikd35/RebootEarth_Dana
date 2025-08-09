# Google Cloud Project Setup for Earth Engine

## Step 1: Create a Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   - Click the project dropdown at the top
   - Click "New Project"
   - Enter a project name (e.g., "alphaearth-crop-recommender")
   - Note the Project ID (it will be auto-generated)
   - Click "Create"

## Step 2: Enable Required APIs

1. **Navigate to APIs & Services**
   - In the left sidebar, go to "APIs & Services" > "Library"

2. **Enable Earth Engine API**
   - Search for "Earth Engine API"
   - Click on it and press "Enable"

3. **Enable other required APIs:**
   - Cloud Resource Manager API
   - Service Usage API
   - Cloud Storage API (optional, for data export)

## Step 3: Set up Authentication

### Option A: Service Account (Recommended for production)

1. **Create Service Account**
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Name: "earth-engine-service"
   - Click "Create and Continue"

2. **Assign Roles**
   - Add role: "Earth Engine Resource Viewer"
   - Add role: "Earth Engine Resource Writer" (if needed)
   - Click "Continue" then "Done"

3. **Create Key**
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create New Key"
   - Choose JSON format
   - Download the key file

### Option B: User Authentication (Easier for development)

1. **Install Google Cloud CLI** (if not already installed)
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Or download from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

## Step 4: Configure Earth Engine

1. **Set Project ID Environment Variable**
   ```bash
   export GOOGLE_CLOUD_PROJECT=your-project-id
   ```

2. **Or add to your shell profile** (~/.zshrc or ~/.bash_profile):
   ```bash
   echo 'export GOOGLE_CLOUD_PROJECT=your-project-id' >> ~/.zshrc
   source ~/.zshrc
   ```

## Step 5: Test the Setup

Run our setup script:
```bash
python setup_earth_engine.py
```

Or test manually:
```bash
python -c "
import ee
import os
project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'your-project-id')
ee.Initialize(project=project_id)
print('✅ Earth Engine initialized successfully!')
"
```

## Common Project IDs to Try

If you don't want to create a new project, you can try these common patterns:
- `your-username-earth-engine`
- `alphaearth-demo`
- `crop-recommender-2024`

## Troubleshooting

### Error: "Project not found"
- Make sure the project ID is correct
- Check that the project is active (not deleted)
- Verify you have access to the project

### Error: "Permission denied"
- Make sure Earth Engine API is enabled
- Check that your account has the necessary roles
- For service accounts, ensure proper key file setup

### Error: "Quota exceeded"
- Earth Engine has usage limits
- Check your quota in the Cloud Console
- Consider upgrading to a paid plan if needed

## Next Steps

Once setup is complete:
1. Run: `python launch_system.py`
2. Choose mode 1 (web interface)
3. Test with real satellite data!

## Security Notes

- Keep service account keys secure
- Don't commit keys to version control
- Use environment variables for sensitive data
- Consider using Google Cloud Secret Manager for production