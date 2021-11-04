// TODO: Write user + server info query
export const userInfoQuery = ``

export const streamCommitsQuery = `
  query($id: String!, $limit: Int, $cursor: String) {
    stream(id: $id){
      name
      updatedAt
      id
      branch(name: "main"){
        commits(limit: $limit, cursor: $cursor) {
          totalCount
          cursor
          items{
            id
            message
            branchName
            sourceApplication
            referencedObject
            authorName
            authorAvatar
            createdAt
          }
        }
      }
    }
  }`

export const streamSearchQuery = `
  query($searchText: String!) {
    streams(query: $searchText) {
      totalCount
      cursor
      items {
        id
        name
        updatedAt
      }
    }
  }`

export const streamObjectQuery = `query($streamId: String!, $objectId: String!) {
    stream(id: $streamId){
        object(id: $objectId){
            totalChildrenCount
            id
            speckleType
            data
        }
    }
}`
export const latestStreamsQuery = `query {
    streams(limit: 10){
        cursor
        totalCount
        items {
            id
            name
            description
            createdAt
            updatedAt
        }
    }
}`
