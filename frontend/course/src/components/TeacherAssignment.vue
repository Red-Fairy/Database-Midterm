<template>
    <div class="assignment-submission">
        <div v-if="error" class="error">{{ error }}</div>
        <h3>作业提交情况：</h3>
        <table>
            <thead>
                <tr>
                    <th class="centered-header">提交ID</th>
                    <th class="centered-header">学生ID</th>
                    <th class="centered-header">提交信息</th>
                    <th class="centered-header">分数</th>
                    <th class="centered-header">操作</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="submission in submissions" :key="submission.submissionID">
                    <td>{{ submission.submissionID }}</td>
                    <td>{{ submission.userID }}</td>
                    <td>{{ submission.submissionInfo }}</td>
                    <td>
                        <input v-model="editSubmissionScore[submission.submissionID]" type="int"
                            :placeholder="submission.submissionScore || '未打分'" />
                    </td>
                    <td>
                        <button @click="scoreSubmission(submission.submissionID)">评分</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>


<script>
import api from '@/api.js';

export default {
    data() {
        return {
            submissions: [],
            editSubmissionScore: {},
            error: "",
        };
    },

    async mounted() {
        const assignmentID = this.$route.params.assignmentID;
        const courseID = this.$route.params.courseID;
        const response = await api.getCourseAssignmentSubmissions(assignmentID, courseID, true);
        if (response.status === "200") {
            this.submissions = response.tabledata;
        } else {
            console.error("Failed to fetch submissions");
        }
    },


    methods: {
        async scoreSubmission(submissionID) {
            console.log('sumissionID:',submissionID);
            const submissionScore = this.editSubmissionScore[submissionID];
            if (submissionScore) {
                const response = await api.updateSubmissionScore(
                    submissionID,
                    submissionScore,
                );
                console.log('response:',response)
                if (response.status === "200") {
                    const submission = this.submissions.find(submission => submission.submissionID === submissionID);
                    submission.submissionScore = submissionScore;
                    this.error = "";
                } else {
                    this.error = "Failed to update submission score";
                    // erase the score from the input box
                    this.editSubmissionScore[submissionID] = "";
                }
                
            }
        },
    },
};
</script>

<style scoped>

.error {
  color: red;
  margin: 10px 0;
}
.assignment-submission {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.assignment-submission h3 {
    margin: 10px 0;
}

.assignment-submission input {
    padding: 6px;
    margin-right: 5px;
    border: 1px solid #ddd;
}

.assignment-submission table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.assignment-submission th,
.assignment-submission td {
    padding: 8px;
    border: 1px solid #ddd;
}

.assignment-submission .centered-header {
    text-align: center;
}

button {
    padding: 6px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

button:not(:last-child) {
    margin-right: 5px;
}
</style>
