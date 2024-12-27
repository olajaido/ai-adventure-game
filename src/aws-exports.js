
// import { fetchAuthSession } from 'aws-amplify/auth';

// const awsExports = {
//     Auth: {
//         Cognito: {
//             region: "eu-west-2",
//             userPoolId: "eu-west-2_EcJ4nZ9ST",
//             userPoolClientId: "2se9lr8i6tolb0ud39u32mvtt9",
//             identityPoolId: "eu-west-2:22500fb6-8ed8-46c7-b05e-bc92bea6e161"
//         }
//     },
//     API: {
//         REST: {
//             gameApi: {
//                 endpoint: "https://hj10g1g5mk.execute-api.eu-west-2.amazonaws.com/dev",  // Will be replaced with actual API Gateway URL
//                 region: "eu-west-2",
//                 custom_header: async () => {
//                     try {
//                         const { tokens } = await fetchAuthSession();
//                         return {
//                             Authorization: `Bearer ${tokens?.idToken?.toString()}`
//                         };
//                     } catch (error) {
//                         console.error('Error fetching auth session:', error);
//                         return {};
//                     }
//                 }
//             }
//         }
//     }
// };

// export default awsExports;

// const awsExports = {
//     Auth: {
//         Cognito: {
//             region: "eu-west-2",
//             userPoolId: "eu-west-2_EcJ4nZ9ST",
//             userPoolClientId: "2se9lr8i6tolb0ud39u32mvtt9",
//             identityPoolId: "eu-west-2:22500fb6-8ed8-46c7-b05e-bc92bea6e161"
//         }
//     },
//     API: {
//         endpoints: [
//             {
//                 name: 'gameApi',
//                 endpoint: 'https://hj10g1g5mk.execute-api.eu-west-2.amazonaws.com/dev',
//                 region: 'eu-west-2'
//             }
//         ]
//     }
// };

// export default awsExports;

// src/aws-exports.js
// src/aws-exports.js
// src/aws-exports.js
const awsExports = {
    aws_project_region: "eu-west-2",
    aws_cognito_region: "eu-west-2",
    aws_user_pools_id: "eu-west-2_EcJ4nZ9ST",
    aws_user_pools_web_client_id: "2se9lr8i6tolb0ud39u32mvtt9",
    aws_cognito_identity_pool_id: "eu-west-2:22500fb6-8ed8-46c7-b05e-bc92bea6e161",
    aws_cloud_logic_custom: [
        {
            name: "gameApi",
            endpoint: "https://hj10g1g5mk.execute-api.eu-west-2.amazonaws.com/dev",
            region: "eu-west-2"
        }
    ]
};

export default awsExports;