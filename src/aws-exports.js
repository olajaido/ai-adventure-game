const awsExports = {
    Auth: {
        region: process.env.REACT_APP_AWS_REGION,
        userPoolId: process.env.REACT_APP_USER_POOL_ID,
        userPoolWebClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
    },
    API: {
        endpoints: [
            {
                name: 'gameApi',
                endpoint: process.env.REACT_APP_LAMBDA_ENDPOINT,
                region: process.env.REACT_APP_AWS_REGION,
                custom_header: async () => {
                    return { Authorization: `Bearer ${(await Auth.currentSession()).getIdToken().getJwtToken()}` }
                }
            }
        ]
    }
};

export default awsExports;