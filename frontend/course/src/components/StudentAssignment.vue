<template>
    <div>
        <h3>提交作业</h3>
        <input v-model="newsubmissionInfo" type="text" placeholder="输入提交信息" />
        <button @click="submitAssignment">提交作业</button>
        <h3>您的作业提交情况：</h3>
        <table>
            <thead>
                <tr>
                    <th>提交ID</th>
                    <th>提交信息</th>
                    <th>分数</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="submission in submissions" :key="submission.submissionID">
                    <td>{{ submission.submissionID }}</td>
                    <td>{{ submission.submissionInfo }}</td>
                    <td>
                        {{ submission.submissionScore }}
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
            newsubmissionInfo: '',
            submissions: [],
            editSubmissionScore: {},
        };
    },

    async mounted() {
        const assignmentID = this.$route.params.assignmentID;
        const courseID = this.$route.params.courseID;
        const userID = this.$route.params.userID;
        console.log('userID:',userID);
        const response = await api.getCourseAssignmentSubmissionsStudent(assignmentID, courseID, userID, false);
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
            console.log('response:',response)
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
