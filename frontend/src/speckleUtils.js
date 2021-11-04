import {
  latestStreamsQuery,
  streamCommitsQuery,
  streamObjectQuery,
  streamSearchQuery,
  userInfoQuery
} from "@/speckleQueries"

export const APP_NAME = process.env.VUE_APP_SPECKLE_NAME
export const SERVER_URL = process.env.VUE_APP_SERVER_URL
export const TOKEN = `${APP_NAME}.AuthToken`
export const REFRESH_TOKEN = `${APP_NAME}.RefreshToken`
export const CHALLENGE = `${APP_NAME}.Challenge`

// Redirects to the Speckle server authentication page, using a randomly generated challenge. Challenge will be stored to compare with when exchanging the access code.
export function goToSpeckleAuthPage() {
  console.log("Redirecting to Speckle Auth page...")
  // TODO: Missing implementation
}

// Log out the current user. This removes the token/refreshToken pair.
export function speckleLogOut() {
  // Remove both token and refreshToken from localStorage
  console.log("Logging out user")
  // TODO: Missing implementation
}

// Exchanges the provided access code with a token/refreshToken pair, and saves them to local storage.
export async function exchangeAccessCode(accessCode) {
  console.log("Exchanging access code...")
  // TODO: Missing implementation
}

// Calls the GraphQL endpoint of the Speckle server with a specific query.
export async function speckleFetch(query, vars) {
  let token = localStorage.getItem(TOKEN)
  if (token)
    try {
      var res = await fetch(`${SERVER_URL}/graphql`, {
        method: "POST",
        headers: {
          Authorization: "Bearer " + token,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: query,
          variables: vars || null
        })
      })
      return await res.json()
    } catch (err) {
      console.error("API call failed", err)
    }
  else return Promise.reject("You are not logged in (token does not exist)")
}

// Fetch the current user data using the userInfoQuery
export const getUserData = () => speckleFetch(userInfoQuery)

// Fetch for streams matching the specified text using the streamSearchQuery
export const searchStreams = e =>
  speckleFetch(streamSearchQuery, { searchText: e })

// Get commits related to a specific stream, allows for pagination by passing a cursor
export const getStreamCommits = (streamId, itemsPerPage, cursor) =>
  speckleFetch(streamCommitsQuery, {
    id: streamId,
    cursor,
    limit: itemsPerPage
  })

export const getObject = (streamId, objectId) =>
  speckleFetch(streamObjectQuery, { streamId, objectId })

export const getStreams = () =>
  speckleFetch(latestStreamsQuery).then(res => res.data?.streams)
