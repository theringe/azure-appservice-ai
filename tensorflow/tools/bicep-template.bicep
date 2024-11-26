param resourcePrefix string = 'tensorflow-bicep-${uniqueString(newGuid())}'

var storageAccountName = '${replace(resourcePrefix, '-', '')}sa'
var storageAccountSkuName = 'Standard_LRS'
var storageAccountPropertiesSupportsHttpsTrafficOnly = true
var storageAccountPropertiesMinimumTlsVersion = 'TLS1_2'
var storageAccountPropertiesDefaultToOAuthAuthentication = true
var storageAccountPropertiesAllowSharedKeyAccess = true
var storageAccountFileservicesPropertiesIsShareSoftDeleteEnabled = true
var storageAccountFileservicesPropertiesShareSoftDeleteRetentionDays = 7
var storageAccountFileShareName = 'data-and-model'
var storageAccountFileShareShareQuota = 5120
var storageAccountFileShareEnabledProtocols = 'SMB'

var planName = '${resourcePrefix}-asp'
var planKind = 'linux'
var planSkuTier = 'Premium0V3'
var planSkuName = 'P0v3'
var planWorkerSize = '0'
var planWorkerSizeId = '0'
var planNumberOfWorkers = 1
var planReserved = true

var appName = '${resourcePrefix}-app'
var appKind = 'app,linux'
var appSiteConfigAppSettingsWEBSITES_CONTAINER_START_TIME_LIMIT = '600'
var appSiteConfigAppSettingsWEBSITES_ENABLE_APP_SERVICE_STORAGE = true
var appSiteConfigAppSettingsSCM_DO_BUILD_DURING_DEPLOYMENT = false
var appSiteConfigLinuxFxVersion = 'PYTHON|3.9'
var appSiteConfigAlwaysOn = true
var appSiteConfigAppCommandLine = '[ -f /home/site/wwwroot/start.sh ] && bash /home/site/wwwroot/start.sh || GUNICORN_CMD_ARGS="--timeout 600 --access-logfile \'-\' --error-logfile \'-\' -c /opt/startup/gunicorn.conf.py --chdir=/opt/defaultsite" gunicorn application:app'
var appSiteConfigFtpsState = 'FtpsOnly'
var appSiteConfigAzureStorageAccountsType = 'AzureFiles'
var appSiteConfigAzureStorageAccountsProtocol = 'Smb'
var appClientAffinityEnabled = false
var appHttpsOnly = true
var appPublicNetworkAccess = 'Enabled'
var appServerFarmId = resourceId('Microsoft.Web/serverfarms', planName)

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-04-01' = {
  name: storageAccountName
  location: resourceGroup().location
  sku: {
    name: storageAccountSkuName
  }
  properties: {
    supportsHttpsTrafficOnly: storageAccountPropertiesSupportsHttpsTrafficOnly
    minimumTlsVersion: storageAccountPropertiesMinimumTlsVersion
    defaultToOAuthAuthentication: storageAccountPropertiesDefaultToOAuthAuthentication
    allowSharedKeyAccess: storageAccountPropertiesAllowSharedKeyAccess
  }
}

resource fileServices 'Microsoft.Storage/storageAccounts/fileServices@2023-04-01' = {
  name: '${storageAccountName}/default'
  dependsOn: [storageAccount]
  properties: {
    shareDeleteRetentionPolicy: {
      enabled: storageAccountFileservicesPropertiesIsShareSoftDeleteEnabled
      days: storageAccountFileservicesPropertiesShareSoftDeleteRetentionDays
    }
  }
}

resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-04-01' = {
  name: '${storageAccountName}/default/${storageAccountFileShareName}'
  location: resourceGroup().location
  dependsOn: [fileServices]
  properties: {
    shareQuota: storageAccountFileShareShareQuota
    enabledProtocols: storageAccountFileShareEnabledProtocols
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2023-12-01' = {
  name: planName
  location: resourceGroup().location
  sku: {
    tier: planSkuTier
    name: planSkuName
  }
  kind: planKind
  properties: {
    reserved: planReserved
    numberOfWorkers: planNumberOfWorkers
    workerSizeId: planWorkerSizeId
  }
}

resource app 'Microsoft.Web/sites@2023-12-01' = {
  name: appName
  location: resourceGroup().location
  kind: appKind
  dependsOn: [appServicePlan]
  properties: {
    serverFarmId: appServerFarmId
    httpsOnly: appHttpsOnly
    publicNetworkAccess: appPublicNetworkAccess
    clientAffinityEnabled: appClientAffinityEnabled
    siteConfig: {
      linuxFxVersion: appSiteConfigLinuxFxVersion
      alwaysOn: appSiteConfigAlwaysOn
      appCommandLine: appSiteConfigAppCommandLine
      ftpsState: appSiteConfigFtpsState
      azureStorageAccounts: {
        '${storageAccountFileShareName}': {
          type: appSiteConfigAzureStorageAccountsType
          accountName: storageAccountName
          shareName: storageAccountFileShareName
          mountPath: '/${storageAccountFileShareName}'
          protocol: appSiteConfigAzureStorageAccountsProtocol
          accessKey: listKeys(storageAccount.id, '2022-05-01').keys[0].value
        }
      }
      appSettings: [
        {
          name: 'WEBSITES_CONTAINER_START_TIME_LIMIT'
          value: appSiteConfigAppSettingsWEBSITES_CONTAINER_START_TIME_LIMIT
        }
        {
          name: 'WEBSITES_ENABLE_APP_SERVICE_STORAGE'
          value: string(appSiteConfigAppSettingsWEBSITES_ENABLE_APP_SERVICE_STORAGE)
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: string(appSiteConfigAppSettingsSCM_DO_BUILD_DURING_DEPLOYMENT)
        }
      ]
    }
  }
}

output outputStorageName string = storageAccountName
output outputShareName string = storageAccountFileShareName
output outputStorageKey string = listKeys(storageAccount.id, '2022-05-01').keys[0].value
