<template>
    <div>
        <h3>作业提交情况：</h3>
        <table>
            <thead>
                <tr>
                    <th>提交ID</th>
                    <th>学生ID</th>
                    <th>提交信息</th>
                    <th>分数</th>
                    <th>操作</th>
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
            console.log(submissionScore);
            if (submissionScore) {
                await api.updateSubmissionScore(
                    submissionID,
                    submissionScore,
                );
                const submission = this.submissions.find(submission => submission.submissionID === submissionID);
                submission.submissionScore = submissionScore;
            }
        },
    },
};
</script>
