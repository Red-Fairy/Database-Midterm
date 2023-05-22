<template>
    <div class="assignment-submission">
        <button>
            <router-link :to="{ name: 'StudentCourse', params: { courseID: $route.params.courseID, userID: $route.params.userID } }" class="button">返回课程</router-link>
        </button>
        <h3>提交作业</h3>
        <div class="input-group">
            <input v-model="newsubmissionInfo" type="text" placeholder="输入提交信息" />
            <button @click="submitAssignment">提交作业</button>
        </div>

        <h3>您的作业提交情况：</h3>
        <table>
            <thead>
                <tr>
                    <th class="centered-header">提交ID</th>
                    <th class="centered-header">提交信息</th>
                    <th class="centered-header">分数</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="submission in submissions" :key="submission.submissionID">
                    <td>{{ submission.submissionID }}</td>
                    <td>{{ submission.submissionInfo }}</td>
                    <td>{{ submission.submissionScore }}</td>
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
            newsubmissionInfo: '',
            submissions: [],
            editSubmissionScore: {},
        };
    },

    async mounted() {
        const assignmentID = this.$route.params.assignmentID;
        const courseID = this.$route.params.courseID;
        const userID = this.$route.params.userID;
        console.log('userID:', userID);
        const response = await api.getCourseAssignmentSubmissionsStudent(courseID, assignmentID, userID, false);
        if (response.status === "200") {
            this.submissions = response.tabledata;
            // if score is null, set it to "未打分"
            for (let i = 0; i < this.submissions.length; i++) {
                if (this.submissions[i].submissionScore === null) {
                    this.submissions[i].submissionScore = "未打分";
                }
            }
        } else {
            console.error("Failed to fetch submissions");
        }
    },

    methods: {
        async submitAssignment() {
            const assignmentID = this.$route.params.assignmentID;
            const courseID = this.$route.params.courseID;
            const userID = this.$route.params.userID;
            const submissionInfo = this.newsubmissionInfo;
            const response = await api.submitAssignment(assignmentID, courseID, userID, submissionInfo);
            this.newsubmissionInfo = '';
            console.log('response:', response)
            const submissionID = response.submissionID;
            this.submissions.push({
                submissionID: submissionID,
                submissionInfo: submissionInfo,
                submissionScore: "未打分",
            });
        },
    }
};
</script>

<style scoped>
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

.assignment-submission .input-group {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}


.assignment-submission button {
    padding: 6px 12px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
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
</style>