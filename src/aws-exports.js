// // import { fetchAuthSession } from 'aws-amplify/auth';

// // const awsExports = {
// //     Auth: {
// //         region: process.env.REACT_APP_AWS_REGION,
// //         userPoolId: process.env.REACT_APP_USER_POOL_ID,
// //         userPoolWebClientId: process.env.REACT_APP_USER_POOL_CLIENT_ID,
// //     },
// //     API: {
// //         REST: {
// //             gameApi: {
// //                 endpoint: process.env.REACT_APP_LAMBDA_ENDPOINT,
// //                 region: process.env.REACT_APP_AWS_REGION,
// //                 custom_header: async () => {
// //                     try {
// //                         const { tokens } = await fetchAuthSession();
// //                         return { 
// //                             Authorization: `Bearer ${tokens?.idToken?.toString()}`
// //                         };
// //                     } catch (error) {
// //                         console.error('Error fetching auth session:', error);
// //                         return {};
// //                     }
// //                 }
// //             }
// //         }
// //     }
// // };

// // export default awsExports;

// // import { fetchAuthSession } from 'aws-amplify/auth';

// // const awsExports = {
// //     Auth: {
// //         region: "eu-west-2",
// //         userPoolId: "eu-west-2_EcJ4nZ9ST",
// //         userPoolWebClientId: "2se9lr8i6tolb0ud39u32mvtt9",
// //     },
// //     API: {
// //         REST: {
// //             gameApi: {
// //                 endpoint: "https://5elzhzvfstykepu5b6h3zccxia0jywml.lambda-url.eu-west-2.on.aws/",
// //                 region: "eu-west-2",
// //                 custom_header: async () => {
// //                     try {
// //                         const { tokens } = await fetchAuthSession();
// //                         return { 
// //                             Authorization: `Bearer ${tokens?.idToken?.toString()}`
// //                         };
// //                     } catch (error) {
// //                         console.error('Error fetching auth session:', error);
// //                         return {};
// //                     }
// //                 }
// //             }
// //         }
// //     }
// // };

// // export default awsExports;

// import { fetchAuthSession } from 'aws-amplify/auth';

// const awsExports = {
//     Auth: {
//         region: "eu-west-2",
//         userPoolId: "eu-west-2_EcJ4nZ9ST",
//         userPoolWebClientId: "2se9lr8i6tolb0ud39u32mvtt9",
//     },
//     API: {
//         REST: {
//             gameApi: {
//                 endpoint: "https://5elzhzvfstykepu5b6h3zccxia0jywml.lambda-url.eu-west-2.on.aws/",
//                 region: "eu-west-2",
//                 custom_header: async () => {
//                     try {
//                         const { tokens } = await fetchAuthSession();
//                         if (!tokens?.idToken) {
//                             throw new Error("ID Token is missing.");
//                         }
//                         return {
//                             Authorization: `Bearer ${tokens.idToken.toString()}`,
//                         };
//                     } catch (error) {
//                         console.error("Error fetching auth session:", error.message);
//                         return {}; // Return an empty header to prevent API request failure
//                     }
//                 },
//             },
//         },
//     },
// };

// export default awsExports;

import { fetchAuthSession } from 'aws-amplify/auth';

const awsExports = {
    Auth: {
        Cognito: {  // Changed to include Cognito namespace
            region: "eu-west-2",
            userPoolId: "eu-west-2_EcJ4nZ9ST",
            userPoolClientId: "2se9lr8i6tolb0ud39u32mvtt9",  // Changed from userPoolWebClientId
            identityPoolId: "eu-west-2:22500fb6-8ed8-46c7-b05e-bc92bea6e161"  // Added identityPoolId if using Identity Pools
        }
    },
    API: {
        REST: {
            gameApi: {
                endpoint: "https://5elzhzvfstykepu5b6h3zccxia0jywml.lambda-url.eu-west-2.on.aws/",
                region: "eu-west-2",
                custom_header: async () => {
                    try {
                        const { tokens } = await fetchAuthSession();
                        return { 
                            Authorization: `Bearer ${tokens?.idToken?.toString()}`
                        };
                    } catch (error) {
                        console.error('Error fetching auth session:', error);
                        return {};
                    }
                }
            }
        }
    }
};

export default awsExports;